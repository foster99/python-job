# This is an auto-generated Django model module.
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    uidentifier = models.CharField(primary_key=True, max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city_name = models.CharField(max_length=255)
    popularity_rate = models.FloatField()
    satisfaction_rate = models.FloatField(blank=True, null=True)
    total_reviews = models.IntegerField()
    average_price = models.FloatField()

    class Meta:
        managed = True
        db_table = 'Restaurant'


class Segment(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    uidentifier = models.CharField(primary_key=True, max_length=255)
    average_popularity_rate = models.FloatField(blank=True, null=True)
    average_satisfaction_rate = models.FloatField(blank=True, null=True)
    average_price = models.FloatField(blank=True, null=True)
    total_reviews = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Segment'


class Restaurant_Segment_Association(models.Model):

    id = models.AutoField(primary_key=True)
    restaurantuid = models.ForeignKey(Restaurant, models.DO_NOTHING, db_column='restaurantUID') 
    segmentuid = models.ForeignKey(Segment, models.DO_NOTHING, db_column='segmentUID')

    class Meta:
        managed = True
        db_table = 'Restaurant_Segment_Association'
        unique_together = (('segmentuid', 'restaurantuid'),)


