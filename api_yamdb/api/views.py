from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import (AdminOnly, IsAdminModeratorPermission,
                          IsadminUserOrReadOnly)

from .serializers import (UserSerializer, NoAdminSerializers,
                          GetTokenSerializers, SignUpSerializers,
                          CategorySerializer, GenreSerializer,
                          TitleCreateUpdateSerializer, TitleSerializer)

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        method=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_serializer_class(sefl, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    pertial=True
                )
            else:
                serializer = NoAdminSerializers(
                    request.user,
                    data=request.data,
                    partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data)


class APISignup(APIView):
    """
    Получить код подтверждения на email.
    Права доступа: без токена.
    Использовать 'me'/'Me'/'I' в username - запрещено.
    Email и username должны быть уникальными
    """
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'{user.username}.'
            f'Код подтверждения: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения.'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_token(request):
    serializer = GetTokenSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    user = get_object_or_404(User, email=email)
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