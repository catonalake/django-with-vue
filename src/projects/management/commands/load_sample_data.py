from django.core.management.base import BaseCommand
from projects.models import Project, Structure, PartDetail


class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        PartDetail.objects.all().delete()
        Structure.objects.all().delete()
        Project.objects.all().delete()

        # Create projects
        self.stdout.write('Creating projects...')

        project1 = Project.objects.create(
            name='Downtown Office Tower',
            description='45-story commercial office building in downtown district'
        )

        project2 = Project.objects.create(
            name='Harbor Bridge Expansion',
            description='Bridge expansion project connecting harbor to mainland'
        )

        # Create structures for Project 1
        self.stdout.write('Creating structures...')

        foundation = Structure.objects.create(
            project=project1,
            name='Foundation',
            description='Building foundation and basement levels'
        )

        parking = Structure.objects.create(
            project=project1,
            name='Parking Garage',
            description='Underground parking structure - 3 levels'
        )

        tower_core = Structure.objects.create(
            project=project1,
            name='Tower Core',
            description='Central elevator and utility core'
        )

        # Create structures for Project 2
        bridge_deck = Structure.objects.create(
            project=project2,
            name='Bridge Deck',
            description='Main driving surface sections'
        )

        support_columns = Structure.objects.create(
            project=project2,
            name='Support Columns',
            description='Vertical support structures'
        )

        # Create part details
        self.stdout.write('Creating part details...')

        # Foundation parts
        PartDetail.objects.create(
            structure=foundation,
            name='Foundation Slab A1',
            price=15000.00,
            takeoff_url='https://s3.example.com/takeoffs/foundation-a1.pdf',
            quantity=4,
            weight=12500.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=foundation,
            name='Foundation Slab A2',
            price=15000.00,
            takeoff_url='https://s3.example.com/takeoffs/foundation-a2.pdf',
            quantity=4,
            weight=12500.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=foundation,
            name='Basement Wall Panel BW-1',
            price=8500.00,
            takeoff_url='https://s3.example.com/takeoffs/basement-wall-1.pdf',
            quantity=12,
            weight=4200.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=foundation,
            name='Basement Wall Panel BW-2',
            price=8500.00,
            takeoff_url='',
            quantity=12,
            weight=4200.00,
            is_released=False  # Not yet released
        )

        # Parking garage parts
        PartDetail.objects.create(
            structure=parking,
            name='Double Tee DT-30',
            price=4200.00,
            takeoff_url='https://s3.example.com/takeoffs/dt-30.pdf',
            quantity=45,
            weight=8500.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=parking,
            name='Double Tee DT-40',
            price=5100.00,
            takeoff_url='https://s3.example.com/takeoffs/dt-40.pdf',
            quantity=30,
            weight=9200.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=parking,
            name='Spandrel Panel SP-1',
            price=3200.00,
            takeoff_url='https://s3.example.com/takeoffs/spandrel-1.pdf',
            quantity=24,
            weight=2800.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=parking,
            name='Column C-1',
            price=2800.00,
            takeoff_url='https://s3.example.com/takeoffs/column-1.pdf',
            quantity=36,
            weight=3500.00,
            is_released=False  # Not yet released
        )

        # Tower core parts
        PartDetail.objects.create(
            structure=tower_core,
            name='Elevator Shaft Panel ES-1',
            price=6500.00,
            takeoff_url='https://s3.example.com/takeoffs/elevator-shaft-1.pdf',
            quantity=90,
            weight=5200.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=tower_core,
            name='Stair Tower Panel ST-1',
            price=4800.00,
            takeoff_url='https://s3.example.com/takeoffs/stair-tower-1.pdf',
            quantity=45,
            weight=3800.00,
            is_released=True
        )

        # Bridge deck parts
        PartDetail.objects.create(
            structure=bridge_deck,
            name='Deck Segment DS-100',
            price=45000.00,
            takeoff_url='https://s3.example.com/takeoffs/deck-segment-100.pdf',
            quantity=8,
            weight=35000.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=bridge_deck,
            name='Deck Segment DS-150',
            price=52000.00,
            takeoff_url='https://s3.example.com/takeoffs/deck-segment-150.pdf',
            quantity=6,
            weight=42000.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=bridge_deck,
            name='Barrier Rail BR-1',
            price=1200.00,
            takeoff_url='https://s3.example.com/takeoffs/barrier-rail-1.pdf',
            quantity=120,
            weight=450.00,
            is_released=False
        )

        # Support column parts
        PartDetail.objects.create(
            structure=support_columns,
            name='Pier Cap PC-1',
            price=28000.00,
            takeoff_url='https://s3.example.com/takeoffs/pier-cap-1.pdf',
            quantity=4,
            weight=22000.00,
            is_released=True
        )
        PartDetail.objects.create(
            structure=support_columns,
            name='Column Segment CS-1',
            price=18000.00,
            takeoff_url='https://s3.example.com/takeoffs/column-segment-1.pdf',
            quantity=16,
            weight=15000.00,
            is_released=True
        )

        # Summary
        self.stdout.write(self.style.SUCCESS(
            f'\nSample data loaded successfully!\n'
            f'  - {Project.objects.count()} projects\n'
            f'  - {Structure.objects.count()} structures\n'
            f'  - {PartDetail.objects.count()} part details'
        ))
