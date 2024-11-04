from django.db import models
import hashlib


class BaseTimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the flowerpot entry was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the flowerpot entry was last updated")
    
    class Meta:
        abstract = True

class Flowerpot(BaseTimeMixin):
    name = models.CharField(max_length=100, unique=True, help_text="Unique name for the smart flowerpot")
    description = models.TextField(blank=True, null=True, help_text="Description or notes about the flowerpot")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Location of the flowerpot (e.g., 'Living Room')")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    

class EnvironmentData(BaseTimeMixin):
    flowerpot: Flowerpot = models.ForeignKey(Flowerpot, on_delete=models.CASCADE, related_name='environment_data', help_text="The flowerpot associated with this data reading")
   
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperature in Celsius", null=True, blank=True)
    moisture = models.DecimalField(max_digits=5, decimal_places=2, help_text="Soil moisture level", null=True, blank=True)
    ph_level = models.DecimalField(max_digits=4, decimal_places=2, help_text="Soil pH level", null=True, blank=True)
    light_level = models.DecimalField(max_digits=5, decimal_places=2, help_text="Light level in lumens", null=True, blank=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Air humidity percentage", null=True, blank=True)
    
    hash = models.CharField(max_length=64, editable=False, unique=True, help_text="Unique log name generated from hash")

    class Meta:
        ordering = ['-created_at']  
        verbose_name = "Environment Data"
        verbose_name_plural = "Environment Data"


    def save(self, *args, **kwargs):
        hash_source = f"{self.flowerpot.name}{self.temperature}{self.moisture}{self.ph_level}{self.light_level}{self.humidity}{self.created_at}"
        self.log_name = hashlib.md5(hash_source.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.flowerpot.name} - {self.log_name}"
    
