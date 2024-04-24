from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .models import Post, Employee


class HomeView(ListView):
    model = Post
    paginate_by = 2
    context_object_name = 'posts'
    ordering = ['-create_at']
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Главная'
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MDigital - Пост'
        return context


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.select_related('category').filter(category__slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        first_post = self.get_queryset().first()
        category_name = first_post.category.name if first_post else None
        context['title'] = f'MDigital - Посты категории {category_name}'
        return context


class PostGridView(ListView):
    model = Post
    paginate_by = 4
    template_name = "blog/post_grid.html"
    context_object_name = 'posts'
    ordering = ['-create_at']

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
        return context

    def get_queryset(self):
        return Post.objects.order_by('-create_at')


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
