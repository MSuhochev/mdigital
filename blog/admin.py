from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from mptt.admin import MPTTModelAdmin
from . import models
from .models import Post, Employee


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name='extends'
            )
        }


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'category', 'author', 'create_at', 'id']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'direction', 'email')
    search_fields = ('first_name', 'last_name', 'position', 'direction', 'email')
    list_filter = ('position', 'direction')


admin.site.register(models.Category, MPTTModelAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)
admin.site.register(Employee, EmployeeAdmin)
