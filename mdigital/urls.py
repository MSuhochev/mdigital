from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from blog.views import Custom404View

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('', include('blog.urls')),
    path('cases/', include('cases.urls')),
    path('career/', include('career.urls')),
    path('webdev/', include('webdev.urls')),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name='blog/robots.txt', content_type='text/plain')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

handler404 = Custom404View.as_view()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
