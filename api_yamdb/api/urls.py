from django.urls import include, path
from rest_framework. routers import SimpleRouter

from .views import UserViewSet, APISignup, send_token

app_name = 'api'

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

auth_patterns = [
    path('token/', send_token),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth', include(auth_patterns)),
]
