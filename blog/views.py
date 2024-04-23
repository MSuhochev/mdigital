from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from .models import Post


class HomeView(ListView):
    model = Post
    paginate_by = 2
    context_object_name = 'posts'
    ordering = ['-create_at']
    template_name = 'index.html'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.select_related('category').filter(category__slug=self.kwargs.get('slug'))


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
        return context

    def get_queryset(self):
        return Post.objects.order_by('-create_at')
