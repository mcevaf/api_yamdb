from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import (AdminOnly, IsAdminModeratorPermission,
                          IsadminUserOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleCreateUpdateSerializer, TitleSerializer,
                          UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',)
    def get_me(sefl, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True)

        if request.method == 'GET':
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(
            serializer.data, status=status.HTTP_200_OK)


class APISignup(APIView):
    """
    ???????????????? ?????? ?????????????????????????? ???? email.
    ?????????? ??????????????: ?????? ????????????.
    ???????????????????????? 'me' ?? username - ??????????????????.
    Email ?? username ???????????? ???????? ??????????????????????
    """
    def send_confirmation_code(self, user):
        send_mail(
            subject='?????????????????????? ???? Yamdb',
            message=(
                '?????? ???????????????????? ?????????????????????? ???? Yamdb ?????????????????? ???????????? '
                f'?? ???????????? ???????????????????????? {user.username} ?? '
                f'?????????? ?????????????????????????? {user.confirmation_code} '
                '???? url - /api/v1/auth/token/.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, _ = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            raise ValidationError(settings.EMAIL_ERROR
                                  if User.objects.filter(email=email).exists()
                                  else settings.USERNAME_ERROR)

        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        self.send_confirmation_code(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(
        {'confirmation_code': '???????????????? ?????? ??????????????????????????!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class CategoryViewSet(ListCreateDeleteViewSet):
    """???????????? ?????? ??????????????????."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDeleteViewSet):
    """???????????? ?????? ????????????."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """???????????? ?????? ????????????????????????."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TitleFilter
    ordering_fields = ('name', 'year',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateUpdateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """???????????? ?????? ???????????? ?? ????????????????."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorPermission,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """???????????? ?????? ???????????? ?? ??????????????????????????."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorPermission,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
