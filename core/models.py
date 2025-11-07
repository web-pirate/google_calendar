from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(
        max_length=7, default="#3788d8", help_text="Hex color (#rrggbb)")
    location = models.CharField(max_length=250, blank=True)
    # Simple recurrence storage — store an RRULE or text describing recurrence.
    recurrence = models.TextField(
        blank=True, help_text="Optional RRULE or recurrence description")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = [
        ("Personal", "Personal"),
        ("Work", "Work"),
        ("Birthday", "Birthday"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="Personal")

    def __str__(self):
        return f"{self.title} ({self.start} - {self.end})"
