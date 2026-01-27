import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Project, Structure, PartDetail, ScheduleEvent, ShippingEvent, ShippingPart


def api_projects_list(request):
    """List all projects."""
    projects = Project.objects.all()
    data = [
        {
            'id': p.id,
            'name': p.name,
            'description': p.description,
        }
        for p in projects
    ]
    return JsonResponse({'data': data})


def api_project_structures(request, project_id):
    """List structures for a project with nested part details."""
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

    structures = project.structures.prefetch_related('part_details').all()
    data = []
    for structure in structures:
        part_details = [
            {
                'id': pd.id,
                'name': pd.name,
                'price': str(pd.price),
                'takeoff_url': pd.takeoff_url,
                'quantity': pd.quantity,
                'weight': str(pd.weight),
                'total_weight': str(pd.total_weight),
                'is_released': pd.is_released,
            }
            for pd in structure.part_details.all()
        ]
        data.append({
            'id': structure.id,
            'name': structure.name,
            'description': structure.description,
            'part_details': part_details,
        })

    return JsonResponse({
        'project': {'id': project.id, 'name': project.name},
        'data': data,
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_schedule_event_create(request):
    """Create a schedule event for a part detail."""
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    required_fields = ['part_detail_id', 'scheduled_date', 'scheduled_time', 'quantity', 'part_identifier', 'price']
    for field in required_fields:
        if field not in body:
            return JsonResponse({'error': f'Missing field: {field}'}, status=400)

    try:
        part_detail = PartDetail.objects.get(id=body['part_detail_id'])
    except PartDetail.DoesNotExist:
        return JsonResponse({'error': 'Part detail not found'}, status=404)

    if not part_detail.is_released:
        return JsonResponse({'error': 'Only released parts can be scheduled'}, status=400)

    schedule_event = ScheduleEvent.objects.create(
        part_detail=part_detail,
        scheduled_date=body['scheduled_date'],
        scheduled_time=body['scheduled_time'],
        quantity=body['quantity'],
        part_identifier=body['part_identifier'],
        price=body['price'],
    )

    return JsonResponse({
        'id': schedule_event.id,
        'part_detail_id': schedule_event.part_detail_id,
        'scheduled_date': str(schedule_event.scheduled_date),
        'scheduled_time': str(schedule_event.scheduled_time),
        'quantity': schedule_event.quantity,
        'part_identifier': schedule_event.part_identifier,
        'price': str(schedule_event.price),
    }, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def api_shipping_event_create(request):
    """Create a shipping event with multiple parts."""
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if 'shipped_date' not in body:
        return JsonResponse({'error': 'Missing field: shipped_date'}, status=400)
    if 'parts' not in body or not isinstance(body['parts'], list):
        return JsonResponse({'error': 'Missing or invalid parts list'}, status=400)

    # Validate all parts exist and are released
    part_ids = [p['part_detail_id'] for p in body['parts']]
    parts = PartDetail.objects.filter(id__in=part_ids)

    if parts.count() != len(part_ids):
        return JsonResponse({'error': 'One or more part details not found'}, status=404)

    unreleased = [p.name for p in parts if not p.is_released]
    if unreleased:
        return JsonResponse({'error': f'Parts not released: {", ".join(unreleased)}'}, status=400)

    # Create shipping event
    shipping_event = ShippingEvent.objects.create(
        shipped_date=body['shipped_date'],
        notes=body.get('notes', ''),
    )

    # Create shipping parts
    total_weight = 0
    shipping_parts_data = []
    for part_data in body['parts']:
        part_detail = parts.get(id=part_data['part_detail_id'])
        weight = part_data.get('weight', part_detail.weight)
        quantity = part_data.get('quantity', 1)

        shipping_part = ShippingPart.objects.create(
            shipping_event=shipping_event,
            part_detail=part_detail,
            quantity=quantity,
            weight=weight,
        )
        total_weight += float(weight) * quantity
        shipping_parts_data.append({
            'id': shipping_part.id,
            'part_detail_id': shipping_part.part_detail_id,
            'part_detail_name': part_detail.name,
            'quantity': shipping_part.quantity,
            'weight': str(shipping_part.weight),
        })

    return JsonResponse({
        'id': shipping_event.id,
        'shipped_date': str(shipping_event.shipped_date),
        'notes': shipping_event.notes,
        'total_weight': str(total_weight),
        'parts': shipping_parts_data,
    }, status=201)


def api_shipping_events_list(request):
    """List all shipping events with totals."""
    events = ShippingEvent.objects.prefetch_related('shipping_parts__part_detail').all()
    data = []
    for event in events:
        parts = [
            {
                'id': sp.id,
                'part_detail_id': sp.part_detail_id,
                'part_detail_name': sp.part_detail.name,
                'quantity': sp.quantity,
                'weight': str(sp.weight),
            }
            for sp in event.shipping_parts.all()
        ]
        data.append({
            'id': event.id,
            'shipped_date': str(event.shipped_date),
            'notes': event.notes,
            'total_weight': str(event.total_weight),
            'parts': parts,
        })

    return JsonResponse({'data': data})
