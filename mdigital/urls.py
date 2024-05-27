from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blog.views import Custom404View

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('', include('blog.urls')),
]

handler404 = Custom404View.as_view()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
