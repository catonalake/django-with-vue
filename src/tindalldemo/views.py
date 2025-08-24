from django.http import JsonResponse
from django.shortcuts import render

def home_view(request):
    return render(request, "home.html")


def api_content_list_view(request):
    """
    this would be a drf endpoint
    """
    content_list = [
        {"id": 1, "title": "Hello World"},
        {"id": 2, "title": "Hello Again World"},
        {"id": 3, "title": "Destination Mars Anyone?"},
        {"id": 4, "title": "Mandelbrots for Everyone"},
    ]
    return JsonResponse({"data": content_list})
