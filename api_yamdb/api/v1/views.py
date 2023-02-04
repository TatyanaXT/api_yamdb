from string import Template

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken

from users.models import CustomUser
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer, \
    MeSerializer
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly

from reviews.models import Category, Genre, Review, Title

from .permissions import AuthorAndModerator, IsAdmin
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    GenreSerializer,
    CategorySerializer,
    TitlesViewSerializer
)

CONFIRMATION_CODE_ERROR = 'Код подтверждения некорректный!'
CONFIRMATION_CODE_EMAIL_SUBJECT = ('YaMdb - Код подтверждения для '
                                   'получения токена')
CONFIRMATION_CODE_EMAIL_MESSAGE = Template(
    'Здравствуйте. Для завершения регистрации на YaMdb используйте '
    'код подтверждения, указанный ниже. '
    'Код подтверждения: $token'
)


class CDLViewSet(mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    """
    Вьюсет для создания, удаления и получения списка.
    """
    pass


class CreateToken(APIView):
    """Вьюсет для создания токена."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        user = get_object_or_404(CustomUser, username=username)

        confirmation_code = serializer.validated_data['confirmation_code']

        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)

            return Response({'token': f'{token}'}, status=HTTP_200_OK)

        return Response(CONFIRMATION_CODE_ERROR, status=HTTP_400_BAD_REQUEST)


class Signup(APIView):
    """Вьюсет для регистрации пользователя."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user = CustomUser.objects.create(username=username, email=email)
        token = default_token_generator.make_token(user)

        send_mail(
            fail_silently=False,
            from_email='test@test.com',
            message=CONFIRMATION_CODE_EMAIL_MESSAGE.substitute(token=token),
            recipient_list=[user.email],
            subject=CONFIRMATION_CODE_EMAIL_MESSAGE,
        )

        return Response(serializer.data, status=HTTP_200_OK)


class UserViewSet(ModelViewSet):
    """Вьюсет для моедли пользователя."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)

    permission_classes = (IsAdmin,)

    search_fields = (
        'username',
    )

    def get_object(self):
        user_username = self.kwargs['pk']
        user = get_object_or_404(CustomUser, username=user_username)
        return user

    @action(
        methods=['get', 'patch', ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        """Метод для заполнения полей в своём профайле пользователем,
        PATCH-запрос на эндпоинт /api/v1/users/me/
        """

        user = CustomUser.objects.get(username=request.user.username)
        serializer = MeSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    """
    Вьюсет для чтения, создания, изменения и удаления отзывов.
    """
    serializer_class = ReviewSerializer
    permission_classes = [
        AuthorAndModerator,
    ]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """
    Вьюсет для чтения, создания, изменения и удаления коментариев.
    """
    serializer_class = CommentSerializer
    permission_classes = [
        AuthorAndModerator,
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(ModelViewSet):
    """Вьюсет для чтения, создания, изменения и удаления title."""
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return TitlesViewSerializer
        return TitleReadSerializer


class GenreViewSet(CDLViewSet):
    """Вьюсет для чтения, создания, изменения и удаления жанра."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CDLViewSet):
    """Вьюсет для чтения, создания, изменения и удаления категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
