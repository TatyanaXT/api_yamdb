from api.v1.urls import api_urlpatterns as api_v1
from django.urls import include, path

urlpatterns = [
    path(r'v1/', include(api_v1)),
]
