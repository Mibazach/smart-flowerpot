from django.db import models
import hashlib
from django.utils import timezone


class BaseTimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=None, blank=None, help_text="Date and time when the flowerpot entry was created")
    updated_at = models.DateTimeField(auto_now=True, null=None, blank=None, help_text="Date and time when the flowerpot entry was last updated")

    class Meta:
        abstract = True


class Flowerpot(BaseTimeMixin):
    name = models.CharField(max_length=100, unique=False, help_text="Unique name for the smart flowerpot")
    slug = models.SlugField(max_length=100, unique=True, help_text="Unique slug for the smart flowerpot")
    description = models.TextField(blank=True, null=True, help_text="Description or notes about the flowerpot")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Location of the flowerpot (e.g., 'Living Room')")

    threshold = models.PositiveIntegerField(
        blank=True, null=True, 
        default=30, help_text="Soil moisture threshold percentage"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class EnvironmentData(BaseTimeMixin):
    flowerpot = models.ForeignKey(
        Flowerpot, 
        on_delete=models.CASCADE, 
        related_name='environment_data', 
        help_text="The flowerpot associated with this data reading"
    )
    hash = models.CharField(
        max_length=64, 
        editable=False, 
        unique=True, 
        help_text="Unique log name generated from hash"
    )
    soil_moisture = models.FloatField(
        blank=True,
        null=True,
        help_text="Soil moisture percentage"
    )
    air_humidity = models.FloatField(
        blank=True,
        null=True,
        help_text="Air humidity percentage"
    )
    temperature = models.FloatField(
        blank=True,
        null=True,
        help_text="Temperature in degrees Celsius"
    )
    class Meta:
        ordering = ['-created_at']  
        verbose_name = "Environment Data"
        verbose_name_plural = "Environment Data"

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        hash_source = f"{self.flowerpot.slug}{self.temperature}{self.soil_moisture}{self.air_humidity}{self.temperature}{self.created_at}"
        self.hash = hashlib.md5(hash_source.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.flowerpot.name} - {self.hash}"
    
