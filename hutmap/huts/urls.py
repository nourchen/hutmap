from django.conf.urls.defaults import *
from django.conf import settings
from tastypie.api import Api

from huts.api import HutResource, RegionResource, AgencyResource

api = Api(api_name='v1')
api.register(HutResource())
api.register(RegionResource())
api.register(AgencyResource())

urlpatterns = patterns('',
  (r'^api/', include(api.urls)),
)
