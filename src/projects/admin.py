from django.contrib import admin
from .models import Project, Structure, PartDetail, ScheduleEvent, ShippingEvent, ShippingPart


class StructureInline(admin.TabularInline):
    model = Structure
    extra = 1


class PartDetailInline(admin.TabularInline):
    model = PartDetail
    extra = 1


class ShippingPartInline(admin.TabularInline):
    model = ShippingPart
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    inlines = [StructureInline]


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'description', 'created_at']
    list_filter = ['project']
    search_fields = ['name', 'description']
    inlines = [PartDetailInline]


@admin.register(PartDetail)
class PartDetailAdmin(admin.ModelAdmin):
    list_display = ['name', 'structure', 'price', 'quantity', 'weight', 'is_released']
    list_filter = ['is_released', 'structure__project']
    search_fields = ['name']


@admin.register(ScheduleEvent)
class ScheduleEventAdmin(admin.ModelAdmin):
    list_display = ['part_identifier', 'part_detail', 'scheduled_date', 'scheduled_time', 'quantity', 'price']
    list_filter = ['scheduled_date', 'part_detail__structure__project']
    search_fields = ['part_identifier']


@admin.register(ShippingEvent)
class ShippingEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'shipped_date', 'notes', 'created_at']
    list_filter = ['shipped_date']
    inlines = [ShippingPartInline]


@admin.register(ShippingPart)
class ShippingPartAdmin(admin.ModelAdmin):
    list_display = ['part_detail', 'shipping_event', 'quantity', 'weight']
    list_filter = ['shipping_event']
