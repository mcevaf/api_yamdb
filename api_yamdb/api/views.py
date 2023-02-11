from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import (AdminOnly, IsAdminModeratorPermission,
                          IsadminUserOrReadOnly)
from .serializers import (UserSerializer,
                          GetTokenSerializer, SignUpSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleCreateUpdateSerializer, TitleSerializer)
from reviews.models import Category, Comment, Genre, Review, Title, User


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
        url_path='me')
    def get_me(sefl, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True)

        if request.method == 'GET':
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class APISignup(APIView):
    """
    Получить код подтверждения на email.
    Права доступа: без токена.
    Использовать 'me' в username - запрещено.
    Email и username должны быть уникальными
    """
    def send_confirmation_code(self, user):
        send_mail(
            subject='Регистрация на Yamdb',
            message=(
                'Для завершения регистрации на Yamdb отправьте запрос '
                f'с именем пользователя {user.username} и '
                f'кодом подтверждения {user.confirmation_code} '
                'на url - /api/v1/auth/token/.'
            ),
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

    permission_classes = (permissions.AllowAny,)

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
        except IntegrityError as error:
            raise ValidationError(
                ('Ошибка при попытке создать новую запись '
                 f'в базе с username={username}, email={email}')
            ) from error
        user.confirmation_code = default_token_generator
        user.save()
        self.send_confirmation_code(user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
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
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


class CategoryViewSet(ListCreateDeleteViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ('=name',)


class GenreViewSet(ListCreateDeleteViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsadminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateUpdateSerializer
        return TitleSerializer
