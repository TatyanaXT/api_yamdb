from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)

title_urlpatterns = [
    path('', include(router.urls))
]
