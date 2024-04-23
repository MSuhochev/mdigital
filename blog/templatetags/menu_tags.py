from django import template
from blog.models import Category

register = template.Library()


@register.inclusion_tag('blog/includes/tags/top_menu.html')
def get_categories():
    category = Category.objects.filter(parent__isnull=True).order_by('id')
    return {'list_category': category}

