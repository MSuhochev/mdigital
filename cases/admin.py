from django.contrib import admin
from .models import Case, CaseCategory
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from mptt.admin import MPTTModelAdmin


class CaseAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Case
        fields = '__all__'
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name='extends'
            )
        }


class CaseAdmin(admin.ModelAdmin):
    form = CaseAdminForm
    list_display = ['title', 'category', 'author', 'create_at', 'slug']
    raw_id_fields = ('author',)
    prepopulated_fields = {'slug': ('title',)}


class CaseCategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


admin.site.register(CaseCategory, CaseCategoryAdmin)
admin.site.register(Case, CaseAdmin)
