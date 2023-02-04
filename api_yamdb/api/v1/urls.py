from rest_framework.routers import DefaultRouter

from .urls_review import review_urlpatterns
from .urls_title import title_urlpatterns
from .urls_users import user_urlpatterns

app_name = 'api'
router = DefaultRouter()

api_urlpatterns = []

api_urlpatterns += user_urlpatterns
api_urlpatterns += title_urlpatterns
api_urlpatterns += review_urlpatterns
