from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APISignup, CategoryViewSet,
                    CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet,
                    UserViewSet, send_token)


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

auth_urls = [
    path('signup/', APISignup.as_view(), name='signup'),
    path('token/', send_token, name='get_token'),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
