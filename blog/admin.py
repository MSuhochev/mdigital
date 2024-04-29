from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django_ckeditor_5.widgets import CKEditor5Widget
from mptt.admin import MPTTModelAdmin
from . import models
from .models import Post, Employee, UserProfile, UserMessage, ContactFormSubmission


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
    raw_id_fields = ('author',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            # Показываем только пользователей, которые связаны с сотрудниками
            kwargs["queryset"] = User.objects.filter(userprofile__employee__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'direction', 'email')
    search_fields = ('first_name', 'last_name', 'position', 'direction', 'email')
    list_filter = ('position', 'direction')


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'message', 'date_sent', 'status')
    search_fields = ('email', 'message')
    list_filter = ('status',)


class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'subject', 'email', 'message', 'created_at', 'status')
    search_fields = ('email', 'message')
    list_filter = ('status',)


admin.site.register(models.Category, MPTTModelAdmin)
admin.site.register(models.Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(ContactFormSubmission, ContactFormSubmissionAdmin)
