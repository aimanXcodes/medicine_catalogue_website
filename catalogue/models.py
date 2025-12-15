from django.db import models, transaction
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# Create your models here.

class MedicineDetail(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='medicine_img/', blank=True, null=True)
    MRP = models.DecimalField(max_digits=10, decimal_places=2)
    formulation = models.CharField(max_length=100)
    ingredients = models.JSONField(blank=True, null=True)
    indications = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# models for offered rates button

class OfferedRates(models.Model):
    image = models.ImageField(upload_to='offered_rates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            OfferedRates.objects.exclude(pk=self.pk).delete()

    def __str__(self):
        return "Offered Rates"


@receiver(post_delete, sender=OfferedRates)
def delete_image_file(sender, instance, **kwargs):
    if not instance.image:
        return

    try:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    except (ValueError, OSError):
        pass


