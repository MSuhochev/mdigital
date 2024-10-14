from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.views.generic import DetailView, ListView
from django.core.exceptions import ObjectDoesNotExist
from blog.forms import ConsultationForm
from .models import Case, CaseCategory


class CaseCategoryMixin:
    @staticmethod
    def get_category_queryset():
        # Получаем все категории кейсов и количество кейсов в каждой категории
        return CaseCategory.objects.annotate(num_cases=Count('cases')).order_by('name')

    @staticmethod
    def get_recent_cases(num_cases=8):
        # Получаем последние кейсы
        return Case.objects.order_by('-create_at')[:num_cases]


class CaseDetailView(CaseCategoryMixin, DetailView):
    model = Case
    context_object_name = 'case'
    slug_url_kwarg = 'case_slug'
    template_name = 'cases/case_detail.html'  # Убедитесь, что шаблон находится в папке 'cases'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.title}'
        context['categories'] = self.get_category_queryset()
        context['recent_cases'] = self.get_recent_cases()

        # Получение предыдущего и следующего кейсов
        current_case = context['case']
        try:
            previous_case = Case.objects.filter(create_at__lt=current_case.create_at).latest('create_at')
        except ObjectDoesNotExist:
            previous_case = None

        try:
            next_case = Case.objects.filter(create_at__gt=current_case.create_at).earliest('create_at')
        except ObjectDoesNotExist:
            next_case = None

        context['previous_case'] = previous_case
        context['next_case'] = next_case
        context['form'] = ConsultationForm()
        return context


class CaseListView(CaseCategoryMixin, ListView):
    model = Case
    paginate_by = 10  # Количество кейсов на страницу
    template_name = "cases/case_list.html"  # Убедитесь, что шаблон находится в папке 'cases'
    context_object_name = 'cases'

    def get_queryset(self):
        # Изменено: используем правильное имя для slug категории
        category_slug = self.kwargs.get('category_slug')
        return Case.objects.select_related('category').filter(category__case_slug=category_slug).order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем category_slug из kwargs
        category_slug = self.kwargs.get('category_slug')

        # Находим категорию по case_slug
        category = CaseCategory.objects.filter(case_slug=category_slug).first()

        # Получаем имя категории для отображения в заголовке
        category_name = category.name if category else "Неизвестная категория"
        context['title'] = f'Проекты категории {category_name}'
        context['form'] = ConsultationForm()

        # Данные о категориях и последние кейсы
        context['categories'] = self.get_category_queryset()
        context['recent_cases'] = self.get_recent_cases()

        return context


class CaseGridView(CaseCategoryMixin, ListView):
    model = Case
    paginate_by = 6
    template_name = "cases/case_grid.html"
    context_object_name = 'cases'
    ordering = ['-create_at']

    def get_queryset(self):
        return Case.objects.order_by('-create_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cases_list = self.get_queryset()

        # Пагинация
        paginator = Paginator(cases_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            cases = paginator.page(page)
        except PageNotAnInteger:
            cases = paginator.page(1)
        except EmptyPage:
            cases = paginator.page(paginator.num_pages)

        context['cases'] = cases
        context['title'] = 'Наши проекты'
        context['categories'] = self.get_category_queryset()
        context['recent_cases'] = self.get_recent_cases()
        context['form'] = ConsultationForm()

        return context


class CaseSearchView(CaseCategoryMixin, ListView):
    model = Case
    template_name = 'case/search_results.html'
    context_object_name = 'cases'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('q')
        # category = self.request.GET.get('category')  # Получаем выбранный раздел из запроса
        queryset = super().get_queryset().order_by('-create_at')  # Получаем базовый QuerySet
        if query:
            queryset = queryset.filter(text__icontains=query)  # Фильтруем по тексту кейса
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

