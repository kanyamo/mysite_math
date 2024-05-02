from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
import os

urlpatterns = [
    path(f'{os.getenv("ADMIN_PATH") or "admin"}/', admin.site.urls),
    path('', include("core.urls")),
    path('accounts/', include('allauth.urls')),
    path('editorjs/', include('django_editorjs_fields.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Django側からの配信はDEBUG時のみ、そうでないときはNginxから行う
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
