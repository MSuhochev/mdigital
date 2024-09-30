import phonenumbers
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, FormView
from .forms import SubscriberForm, ConsultationForm, CostCalculationForm
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
        context['title'] = 'Telegram боты - Веб-Разработка - Динамическая монетизация сайтов'
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
        return render(request, 'blog/404.html', status=404)


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
        except ObjectDoesNotExist:
            previous_post = None

        try:
            next_post = Post.objects.filter(create_at__gt=current_post.create_at).earliest('create_at')
        except ObjectDoesNotExist:
            next_post = None

        context['previous_post'] = previous_post
        context['next_post'] = next_post
        context['form'] = ConsultationForm()
        return context


class PostListView(CategoryMixin, ListView):
    model = Post
    paginate_by = 3
    template_name = "blog/post_list.html"

    def get_category(self):
        if not hasattr(self, 'category'):
            category_slug = self.kwargs.get('slug')
            self.category = get_object_or_404(Category, slug=category_slug)
        return self.category

    def get_queryset(self):
        category = self.get_category()
        return Post.objects.select_related('category').filter(category=category).order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context['title'] = f'Посты категории {category.name}'
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['total_posts'] = paginator.count
        context['categories'] = self.get_category_queryset()
        context['recent_posts'] = self.get_recent_posts()
        context['form'] = ConsultationForm()
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
        context['title'] = 'Все Посты'
        context['form'] = ConsultationForm()
        context['categories'] = self.get_category_queryset()
        context['recent_posts'] = self.get_recent_posts()
        return context


class AboutView(ListView):
    model = Employee
    template_name = "blog/about.html"
    paginate_by = 4

    def get_queryset(self):
        # Сортируем сотрудников по ID
        return Employee.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        context['form'] = ConsultationForm()

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
        context['title'] = 'Контакты'
        context['form'] = ConsultationForm()
        return context


class MonetizationView(ListView):
    model = Post
    template_name = "blog/monetization.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Динамическая монетизация сайтов'
        context['form'] = ConsultationForm()
        return context


class TelegramDevelopmentView(ListView):
    model = Post
    template_name = "blog/tg_development.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Разработка в Telegram'
        context['form'] = ConsultationForm()
        return context


class AnalyticsView(ListView):
    model = Post
    template_name = "blog/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аналитика'
        context['form'] = ConsultationForm()
        return context


class SupportView(ListView):
    model = Post
    template_name = "blog/support.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поддержка'
        context['form'] = ConsultationForm()
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
        context['title'] = 'Результат поиска'
        context['form'] = ConsultationForm()

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
    telegram_bot_token = 'TOKEN'

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


class CostCalculationView(BaseTelegramNotificationView):
    telegram_chat_id = '-1002178365833'
    template_name = "blog/tg_development.html"

    def post(self, request, *args, **kwargs):
        form = CostCalculationForm(request.POST)
        if form.is_valid():
            # Сохраняем форму, но не отправляем в базу данных сразу
            cost_request = form.save(commit=False)
            # Отправляем сообщение в Telegram
            message = (f"Новая заявка:\nИмя: {cost_request.name}\nТелефон: {cost_request.phone}\n"
                       f"Ниша: {cost_request.niche}\nФункционал: {cost_request.functionality}")
            self.send_telegram_message(message)
            # Теперь сохраняем в базу данных
            cost_request.save()
            return JsonResponse({'success': True, 'message': 'Заявка принята, мы свяжемся с вами в ближайшее время.'})
        return JsonResponse({'success': False, 'message': 'Ошибка в заполнении формы.'})


class PrivacyPolicyView(TemplateView):
    template_name = 'blog/privacy_policy.html'


class ConsultationRequestView(BaseTelegramNotificationView, FormView):
    telegram_chat_id = '-1002229106132'
    form_class = ConsultationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        consultation = form.save()

        # Отправка данных в Telegram
        message_text = (
            f"Новая заявка на консультацию:\n"
            f"Имя: {consultation.name}\n"
            f"Телефон: {consultation.phone}\n"
            f"Удобное время: {consultation.preferred_time}\n"
        )
        self.send_telegram_message(message_text)

        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


class CookieConsentView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = JsonResponse({'status': 'success'})
        response.set_cookie('cookie_consent', 'yes', max_age=365 * 24 * 60 * 60)  # Устанавливаем куку на 1 год
        return response
