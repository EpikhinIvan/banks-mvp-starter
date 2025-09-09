from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    bic = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=80, db_index=True)
    city = models.CharField(max_length=80, blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    swift = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    site = models.URLField(blank=True)

    def __str__(self):
        return self.name
