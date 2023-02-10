from django.urls import include, path
from rest_framework. routers import DefaultRouter

from .views import (UserViewSet, APISignup, CategoryViewSet,
                    GenreViewSet, TitleViewSet, send_token)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', send_token, name='get_token'),
]
