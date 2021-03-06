from csv import DictReader
from datetime import datetime
from django.core.management.base import BaseCommand
from huts.models import Hut, Region, Agency
from huts.utils.null_na import from_csv, DB_NA_POS_NUM, DB_NA_STRING, DB_NA_LIST, CSV_NA, CSV_NULL
from huts.utils.countries import lookup_country_code


class Command(BaseCommand):
  args = '<csvfile>'
  help = 'Imports the given csvfile into the database.'

  def handle(self, *args, **options):
    if len(args) == 1:

      with open(args[0], 'r') as csvfile:
        reader = DictReader(csvfile)
        for values in reader:
          save_agency(values)

      with open(args[0], 'r') as csvfile:
        reader = DictReader(csvfile)
        for values in reader:
          save_hut(values)


def get(values, key, val_na, val_eval):
  value = values[key]
  return from_csv(value, val_na, val_eval)

def get_string(values, key):
  return get(values, key, DB_NA_STRING, lambda x: x)

def get_datetime(values, key):
  return get(values, key, None, 
      lambda x: datetime.strptime(x, '%Y-%m-%d'))

def get_list(values, key):
  return get(values, key, DB_NA_LIST, lambda x: x.split(','))

def get_bool(values, key):
  return get(values, key, None, lambda x: x == '1')

def get_pos_int(values, key):
  return get(values, key, DB_NA_POS_NUM, lambda x: int(x))

def get_pos_float(values, key):
  return get(values, key, DB_NA_POS_NUM, lambda x: float(x))

def get_float(values, key):
  return get(values, key, None, lambda x: float(x))

def save_agency(values):
  agency_parent = get_string(values, 'agency_parent')
  parent_agency = None
  if agency_parent:
    parent_agency, created = Agency.objects.get_or_create(
      name = agency_parent,
    )

  agency_name = get_string(values, 'agency_name')
  if agency_name:
    agency, created = Agency.objects.get_or_create(
      name = agency_name,
      parent = parent_agency,
    )
    agency.url = get_string(values, 'agency_url')
    agency.save()


def save_hut(values):
  # only save huts from WA and CO
  #state = values['state']
  #if state not in ['Washington', 'Colorado']:
  #  return

  if not values['latitude'] or not values['longitude']:
    return

  try:
    region_name = get_string(values, 'region')
    region = None
    if region_name:
      region, created = Region.objects.get_or_create(
        region=region_name
      )

    agency_name = get_string(values, 'agency_name')
    agency = None
    if agency_name:
      agency = Agency.objects.get(name=get_string(values, 'agency_name'))

    hut, created = Hut.objects.get_or_create(
      updated = get_datetime(values, 'date_updated'),
      discretion = get_bool(values, 'discretion'),

      location = 'POINT({0} {1})'.format(get_float(values, 'longitude'), get_float(values, 'latitude')),
      altitude_meters = get_pos_int(values, 'altitude_meters'),
      location_accuracy = get_pos_int(values, 'location_accuracy'),
      show_satellite = get_bool(values, 'show_satellite'),
      location_references = get_list(values, 'location_references'),

      country = lookup_country_code(get_string(values, 'country')),
      state = get_string(values, 'state'),
      region = region,
      designations = get_list(values, 'designations'),
      systems = get_list(values, 'systems'),

      agency = agency,

      name = get_string(values, 'name'),
      alternate_names = get_list(values, 'alternate_names'),
      hut_url = get_string(values, 'hut_url'),
      photo_url = get_string(values, 'photo_url'),
      photo_credit_name = get_string(values, 'photo_credit_name'),
      photo_credit_url = get_string(values, 'photo_credit_url'),
      backcountry = get_pos_int(values, 'backcountry'),
      open_summer = get_bool(values, 'open_summer'),
      open_winter = get_bool(values, 'open_winter'),

      access_no_snow = get_list(values, 'access_no_snow'),
      no_snow_min_km = get_pos_float(values, 'no_snow_min_km'),
      snow_min_km = get_pos_float(values, 'snow_min_km'),

      types = get_list(values, 'types'),
      structures = get_pos_int(values, 'structures'),

      capacity_max = get_pos_int(values, 'capacity_max'),
      capacity_hut_min = get_pos_int(values, 'capacity_hut_min'),
      capacity_hut_max = get_pos_int(values, 'capacity_hut_max'),

      fee_person_min = get_pos_float(values, 'fee_person_min'),
      fee_person_max = get_pos_float(values, 'fee_person_max'),
      fee_person_occupancy_min  =  get_pos_int(values, 'fee_person_occupancy_min'),
      fee_hut_min = get_pos_float(values, 'fee_hut_min'),
      fee_hut_max = get_pos_float(values, 'fee_hut_max'),
      fee_hut_occupancy_max = get_pos_int(values, 'fee_hut_occupancy_max'),

      services_included = get_list(values, 'services_included'),
      optional_services_available = get_bool(values, 'optional_services_available'),
      restriction = get_string(values, 'restriction'),
      reservations = get_bool(values, 'reservations'),
      locked = get_bool(values, 'locked'),
      overnight = get_bool(values, 'overnight'),
      private = get_bool(values, 'private'),
      published = get_bool(values, 'published'),
    )
  except Exception as e:
    print('Failure!: {0}'.format(e.args))
    print('Failed row was: {0}'.format(values))

