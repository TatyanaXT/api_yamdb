from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

SCORE_ERROR = 'Оценка по 10-бальной шкале!'
REVIEW_ERROR = 'Пользователь может оставить только один отзыв!'
NAME_ME_ERROR = 'Использовать "me" в качестве имени пользователя недопустимо!'

CONFIRMATION_CODE_NAX_LENGTH = 50


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )
        model = Title


class TitlesViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        user = self.context['request'].user
        title_id = self.context.get('view').kwargs.get('title_id')
        if (
            request.method == 'POST'
            and user.reviews.filter(title_id=title_id).exists()
        ):
            raise ValidationError(REVIEW_ERROR)
        return data

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для SignUp. ПРедусмотрена проверка на недопустимое имя."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(NAME_ME_ERROR)

        return value


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для Token."""
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_NAX_LENGTH,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомой модели пользователя."""

    class Meta:
        model = CustomUser

        fields = (
            'bio',
            'email',
            'first_name',
            'last_name',
            'role',
            'username',
        )


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'bio',
            'email',
            'first_name',
            'last_name',
            'role',
            'username',
        )
