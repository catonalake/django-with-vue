from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Structure(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='structures'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class PartDetail(models.Model):
    structure = models.ForeignKey(
        Structure, on_delete=models.CASCADE, related_name='part_details'
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    takeoff_url = models.URLField(blank=True, help_text="S3 link to takeoff document")
    quantity = models.PositiveIntegerField(default=1)
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight per unit")
    is_released = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.structure.name} - {self.name}"

    @property
    def total_weight(self):
        return self.weight * self.quantity


class ScheduleEvent(models.Model):
    part_detail = models.ForeignKey(
        PartDetail, on_delete=models.CASCADE, related_name='schedule_events'
    )
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    quantity = models.PositiveIntegerField(default=1)
    part_identifier = models.CharField(
        max_length=255, help_text="Can differ from original part detail name"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Can differ from original price"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.part_identifier} @ {self.scheduled_date} {self.scheduled_time}"

    class Meta:
        ordering = ['-scheduled_date', '-scheduled_time']


class ShippingEvent(models.Model):
    shipped_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment {self.id} - {self.shipped_date}"

    @property
    def total_weight(self):
        return sum(sp.weight * sp.quantity for sp in self.shipping_parts.all())

    class Meta:
        ordering = ['-shipped_date']


class ShippingPart(models.Model):
    shipping_event = models.ForeignKey(
        ShippingEvent, on_delete=models.CASCADE, related_name='shipping_parts'
    )
    part_detail = models.ForeignKey(
        PartDetail, on_delete=models.CASCADE, related_name='shipping_parts'
    )
    quantity = models.PositiveIntegerField(default=1)
    weight = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Weight at time of shipment"
    )

    def __str__(self):
        return f"{self.part_detail.name} x{self.quantity}"
