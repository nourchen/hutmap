from django.contrib.gis.db import models
from util.countries import CountryField

class Hut(models.Model):
  LOCATION_ACCURACY_CHOICES = (
    (0, 'wild ass guess'), 
    (1, 'hut not found on map, only word description of location'), 
    (2, 'hut not found on imagery or topo, but location eyeballed from agency \
     provided static map'), 
    (3, 'hut located on satellite view in Google Maps or on topo'), 
    (4, 'surveyed in situ'), 
    (None, 'coordinates provided and yet unverified')
  )

  ACCESS_CHOICES = (
    (0, 'frontcountry year-round'),
    (1, 'winter backcountry'),
    (2, 'backcountry year-round')
  )

  # metadata
  created = models.DateField(auto_now_add=True)
  updated = models.DateField(auto_now=True)
  # location
  region = models.ForeignKey('Region')
  location = models.PointField()
  location_accuracy = models.IntegerField(choices=LOCATION_ACCURACY_CHOICES, 
                                         null=True, blank=True)
  altitude = models.IntegerField('altitude (m)',
                                null=True, blank=True)
  # details
  name = models.CharField(max_length=100)
  access = models.IntegerField(choices=ACCESS_CHOICES)
  type = models.ForeignKey('HutType')
  num_structures = models.IntegerField('number of structures')
  # capacity
  capacity_max = models.IntegerField('total capacity')
  capacity_hut_min = models.IntegerField('minimum hut capacity')
  capacity_hut_max = models.IntegerField('maximum hut capacity')
  # fees
  fee_person_min = models.FloatField('minimum fee per person per night',
                                     null=True, blank=True)
  fee_person_max = models.FloatField('maximum fee per person per night',
                                     null=True, blank=True)
  fee_hut_min = models.FloatField('minimum fee per hut per night',
                                  null=True, blank=True)
  fee_hut_max = models.FloatField('maximum fee per hut per night',
                                  null=True, blank=True)
  reservations = models.BooleanField('reservations accepted')
  # urls
  hut_url = models.URLField()
  photo_url = models.URLField()
  references = models.CharField(max_length=200)
  # agency
  agency = models.ForeignKey('Agency')
  # for geodjango
  objects = models.GeoManager()

  def __unicode__(self):
    return self.name

class Region(models.Model):
  country = CountryField()
  state = models.CharField(max_length=20, blank=True)
  region = models.CharField(max_length=50)
  area = models.PolygonField(null=True, spatial_index=False)
  objects = models.GeoManager()

  def __unicode__(self):
    return '{0}, {1}, {2}'.format(self.region, self.state, self.country)

class Agency(models.Model):
  name = models.CharField(max_length=100)
  url = models.URLField()
  objects = models.GeoManager()

  def __unicode__(self):
    return self.name

class HutType(models.Model):
  name = models.CharField(max_length=50, primary_key=True)
  objects = models.GeoManager()

  def __unicode__(self):
    return self.name