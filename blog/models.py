from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    image = models.ImageField(upload_to='articles/', verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст')
    category = models.ForeignKey(
        Category,
        related_name='post',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    tag = models.ManyToManyField(Tag, related_name='posts', verbose_name='Теги')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(max_length=200, default=None, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_single', kwargs={'slug': self.category.slug, 'post_slug': self.slug})
