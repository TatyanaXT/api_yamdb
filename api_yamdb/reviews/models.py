from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser

MAX_LENGTH_NAME = 80
MAX_LENGTH_SLUG = 25


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField('Название', max_length=MAX_LENGTH_NAME)
    slug = models.SlugField(max_length=MAX_LENGTH_SLUG, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_NAME)

    slug = models.SlugField(
        'Cлаг',
        max_length=MAX_LENGTH_SLUG,
        unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений (фильмы/книги/музыка)."""

    name = models.CharField('Название', max_length=MAX_LENGTH_NAME)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category, related_name='titles', on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )
    pub_date = models.DateTimeField(
        'Дата отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для хранения комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
