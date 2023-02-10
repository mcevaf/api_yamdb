from django.urls import include, path
from rest_framework. routers import SimpleRouter, DefaultRouter

from .views import (UserViewSet, APISignup, CategoryViewSet,
                    GenreViewSet, TitleViewSet, send_token)

app_name = 'api'

# router_v1 = DefaultRouter()
router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

auth_patterns = [
    path('token/', send_token),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth', include(auth_patterns)),
]

#urlpatterns = [
#    path('v1/', include(router_v1.urls)),
#]
