from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateToken, Signup, UserViewSet

router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

token_auth_urls = [
    path(
        'auth/signup/',
        Signup.as_view(),
        name='signup'
    ),
    path(
        'auth/token/',
        CreateToken.as_view(),
        name='obtain_token'
    ),
]

user_urlpatterns = [

    path('', include(router.urls)),
    path('', include(token_auth_urls)),
]
