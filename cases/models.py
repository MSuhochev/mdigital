from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class CaseCategory(MPTTModel):
    name = models.CharField(max_length=100, verbose_name='Название')
    case_slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг категории кейса')
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
        verbose_name = 'Категория кейсов'
        verbose_name_plural = 'Категории кейсов'

    def __str__(self):
        return self.name


class Case(models.Model):
    author = models.ForeignKey(User, related_name='cases', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    image = models.ImageField(upload_to='cases/', verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст')
    category = models.ForeignKey(
        CaseCategory,
        related_name='cases',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(max_length=200, default=None, unique=True, verbose_name='Слаг')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('case_detail', kwargs={
            'category_slug': self.category.case_slug,
            'case_slug': self.slug
        })
