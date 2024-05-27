import phonenumbers
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import SubscriberForm
from .models import Post, Employee, Category, UserMessage, IncomingOrders, ContactFormSubmission
import requests


class HomeView(ListView):
    model = Post
    paginate_by = 2
    context_object_name = 'posts'
    ordering = ['-create_at']
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Telegram боты - Веб-Разработка - Динамическая монетизация | mdigital.su'
        context['form'] = SubscriberForm()  # Добавляем форму подписки в контекст
        return context

    def post(self, request, *args, **kwargs):
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно подписались на рассылку")
            return JsonResponse({'message': "Вы успешно подписались на рассылку"})
        else:
            messages.error(request, "Произошла ошибка при подписке")
            return JsonResponse({'message': "Произошла ошибка при подписке"})


class Custom404View(View):
    def get(self, request, *args, **kwargs):
        return render(request, '404.html', status=404)


class CategoryMixin:
    @staticmethod
    def get_category_queryset():
        # Получаем все категории и количество постов в каждой категории
        return Category.objects.annotate(num_posts=Count('post')).order_by('name')

    @staticmethod
    def get_recent_posts(num_posts=8):
        # Получаем последние статьи
        return Post.objects.order_by('-create_at')[:num_posts]


class PostDetailView(CategoryMixin, DetailView):
    model = Post
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.title}'
        context['categories'] = self.get_category_queryset()
        context['recent_posts'] = self.get_recent_posts()
        # Получение предыдущего и следующего постов
        current_post = context['post']
        try:
            previous_post = Post.objects.filter(create_at__lt=current_post.create_at).latest('create_at')
        except Post.DoesNotExist:
            previous_post = None

        try:
            next_post = Post.objects.filter(create_at__gt=current_post.create_at).earliest('create_at')
        except Post.DoesNotExist:
            next_post = None

        context['previous_post'] = previous_post
        context['next_post'] = next_post
        return context


class PostListView(CategoryMixin, ListView):
    model = Post
    paginate_by = 3  # Устанавливаем количество постов на страницу
    template_name = "blog/post_list.html"

    def get_queryset(self):
        return Post.objects.select_related('category').filter(category__slug=self.kwargs.get('slug')).order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.get_queryset().first().category.name if self.get_queryset().exists() else None
        context['title'] = f'MDigital - Посты категории {category_name}'
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['total_posts'] = paginator.count
        context['categories'] = self.get_category_queryset()
        context['recent_posts'] = self.get_recent_posts()
        return context


class PostGridView(CategoryMixin, ListView):
    model = Post
    paginate_by = 4
    template_name = "blog/post_grid.html"
    context_object_name = 'posts'
    ordering = ['-create_at']

    def get_queryset(self):
        return Post.objects.order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts_list = Post.objects.all().order_by('-create_at')
        paginator = Paginator(posts_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        context['title'] = 'MDigital - Все Посты'
        context['categories'] = self.get_category_queryset()
        context['recent_posts'] = self.get_recent_posts()
        return context


class AboutView(ListView):
    model = Employee
    template_name = "blog/about.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - О нас'

        # Получаем queryset сотрудников, отсортированный по ID
        employees = Employee.objects.all().order_by('id')

        # Применяем пагинацию к списку сотрудников
        paginator = Paginator(employees, self.paginate_by)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except Exception as e:
            page_obj = paginator.get_page(1)

        context['employees'] = page_obj  # Добавляем объект страницы с сотрудниками в контекст
        return context


class ContactsView(ListView):
    model = Post
    template_name = "blog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Контакты'
        return context


class MonetizationView(ListView):
    model = Post
    template_name = "blog/monetization.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Динамическая монетизация'
        return context


class TelegramDevelopmentView(ListView):
    model = Post
    template_name = "blog/tg_development.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Разработка в Telegram'
        return context


class WebDevelopmentView(ListView):
    model = Post
    template_name = "blog/web_development.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - WEB Разработка'
        return context


class AnalyticsView(ListView):
    model = Post
    template_name = "blog/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Аналитика'
        return context


class SupportView(ListView):
    model = Post
    template_name = "blog/support.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Поддержка'
        return context


class ProjectsGridView(ListView):
    template_name = "blog/projects.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Наши проекты'
        return context


class CareerView(ListView):
    model = Post
    template_name = "blog/career.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Карьера'
        return context


class PostSearchView(CategoryMixin, ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        # category = self.request.GET.get('category')  # Получаем выбранный раздел из запроса

        queryset = super().get_queryset().order_by('-create_at')  # Получаем базовый QuerySet

        if query:
            queryset = queryset.filter(text__icontains=query)  # Фильтруем по тексту поста

        # if category:
        #     queryset = queryset.filter(category=category)  # Фильтруем по выбранному разделу

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        context['title'] = 'MDigital - Результат поиска'

        paginator = context.get('paginator')
        page = context.get('page_obj')

        if paginator and page:
            # Вычисляем общее количество элементов на предыдущих страницах
            total_previous_items = paginator.per_page * (page.number - 1)
            # Вычисляем общий номер элемента на текущей странице
            total_start_index = total_previous_items + 1
            context['total_start_index'] = total_start_index

        return context


class BaseTelegramNotificationView(View):
    telegram_bot_token = 'token'

    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            'chat_id': self.telegram_chat_id,
            'text': message
        }
        response = requests.post(url, json=payload)
        return response.json()


class SubmitQuestionView(BaseTelegramNotificationView):
    telegram_chat_id = '-1002053479136'

    def post(self, request):
        email = request.POST.get('email')
        message = request.POST.get('message')

        UserMessage.objects.create(
            email=email,
            message=message,
            date_sent=timezone.now(),
            status='pending'
        )
        message_text = f"Новое сообщение от: {email}\n\n{message}"
        self.send_telegram_message(message_text)

        response_data = {'message': "Спасибо за ваш вопрос! Ответим в ближайшее время"}
        return JsonResponse(response_data)


class IncomingOrdersView(BaseTelegramNotificationView):
    telegram_chat_id = '-1002003513414'

    def post(self, request):
        email = request.POST.get('email')
        site = request.POST.get('site')

        IncomingOrders.objects.create(
            email=email,
            site=site,
            date_sent=timezone.now(),
            status='pending'
        )
        message_text = f"Новая заявка: {email}\n\n{site}"
        self.send_telegram_message(message_text)

        response_data = {'message': "Спасибо за ваше обращение! Рассмотрим в ближайшее время"}
        return JsonResponse(response_data)


class ContactFormSubmitView(BaseTelegramNotificationView):
    telegram_chat_id = '-1002053479136'

    def post(self, request):
        # Обработка данных формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            parsed_phone = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed_phone):
                # Если номер телефона недействителен, возвращаем ошибку
                response_data = {'message': 'Пожалуйста, введите корректный номер телефона'}
                return JsonResponse(response_data)
        except phonenumbers.phonenumberutil.NumberParseException:
            # Если возникла ошибка при разборе номера телефона, также возвращаем ошибку
            response_data = {'message': 'Пожалуйста, введите корректный номер телефона'}
            return JsonResponse(response_data)

        message_text = f"Новое сообщение от: {name}\n\n{email}\n\n{message}"
        self.send_telegram_message(message_text)

        # Далее обработайте данные по вашим потребностям, например, сохраните их в базе данных
        ContactFormSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )

        response_data = {'message': "Спасибо за сообщение! Ответим в ближайшее время"}
        return JsonResponse(response_data)
