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
        category_slug = self.category.slug if self.category else 'no-category'
        return reverse('post_single', kwargs={'slug': self.category.slug, 'post_slug': self.slug})


class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    position = models.CharField(max_length=100, verbose_name='Должность')
    direction = models.CharField(max_length=100, verbose_name='Направление')
    quote = models.CharField(max_length=200, verbose_name='Девиз', blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True, verbose_name='Phone')
    email = models.EmailField(verbose_name='E-mail')
    telegram_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='Telegram ID')
    vk_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='VK ID')
    photo = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username if self.user else ''


class UserMessage(models.Model):
    email = models.EmailField()
    message = models.TextField(verbose_name='Сообщение')
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('done', 'Done')], default='pending', verbose_name='Статус')

    class Meta:
        verbose_name = 'Вопрос пользователя'
        verbose_name_plural = 'Вопросы пользователей'

    def __str__(self):
        return f"Message from {self.email} sent on {self.date_sent}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка на рассылку'

    def __str__(self):
        return self.email


class IncomingOrders(models.Model):
    site = models.CharField(max_length=200, verbose_name='Сайт')
    email = models.EmailField()
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('done', 'Done')], default='pending', verbose_name='Статус')

    class Meta:
        verbose_name = 'Заявка на монетизацию'
        verbose_name_plural = 'Заявки на монетизацию'

    def __str__(self):
        return f"Message from {self.email} sent on {self.date_sent}"


class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('done', 'Done')], default='pending',
                              verbose_name='Статус')

    class Meta:
        verbose_name = 'Сообщение пользователя'
        verbose_name_plural = 'Сообщения пользователей'

    def __str__(self):
        return self.subject
