from django.db import models

# Create your models here.
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    all_day = models.BooleanField(default=False)

    def _str_(self):
        return self.title