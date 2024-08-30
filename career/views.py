from django.views.generic import ListView

from blog.forms import ConsultationForm
from blog.models import Post


class CareerView(ListView):
    model = Post
    template_name = "career/career.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Карьера'
        context['form'] = ConsultationForm()
        return context

