from django.db import models

class ColdStorage(models.Model):
    project_name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.FloatField(help_text="Capacity in MT", null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    project_cost = models.FloatField(null=True, blank=True)
    grant_released = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.project_name

class Scheme(models.Model):
    name = models.CharField(max_length=255)
    ministry = models.CharField(max_length=255, default="Ministry of Food Processing Industries")
    eligibility = models.TextField()
    benefits = models.TextField()
    application_process = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class CropProduction(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    crop = models.CharField(max_length=100)
    season = models.CharField(max_length=50, null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    production = models.FloatField(null=True, blank=True)
    year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.crop} in {self.district}, {self.state} ({self.year})"
