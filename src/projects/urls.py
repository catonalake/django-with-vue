from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.api_projects_list, name='api_projects_list'),
    path('projects/<int:project_id>/structures/', views.api_project_structures, name='api_project_structures'),
    path('schedule-events/', views.api_schedule_event_create, name='api_schedule_event_create'),
    path('shipping-events/', views.api_shipping_events_list, name='api_shipping_events_list'),
    path('shipping-events/create/', views.api_shipping_event_create, name='api_shipping_event_create'),
]
