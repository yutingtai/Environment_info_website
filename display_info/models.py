from django.db import models


# Create your models here.
class AqiDataDbModel(models.Model):
    station_lat = models.FloatField()
    station_lon = models.FloatField()
    aqi_value = models.IntegerField()
    aqi_time = models.CharField(max_length=30,default="")


class EqDataDbModel(models.Model):
    epi_lat = models.FloatField()
    epi_lon = models.FloatField()
    eq_magnitude = models.FloatField(default=0)
    eq_time = models.CharField(max_length=30)


class IntensityDbModel(models.Model):
    shaking_area_lat = models.FloatField()
    shaking_area_lon = models.FloatField()
    seismic_intensity = models.CharField(max_length=5)
    id_earthquake = models.ForeignKey(EqDataDbModel, on_delete=models.CASCADE)
