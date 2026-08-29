from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_control
from django.views.static import serve as serve_static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls')),
]

# django.conf.urls.static.static() is a no-op unless DEBUG=True, so it can't
# be used here: on Vercel DEBUG is off but the media/ dir still ships as part
# of the deployment bundle and needs to be served directly by the app.
# Photo files are immutable once uploaded (each upload gets its own path), so
# a long-lived cache means repeat visits don't re-download the same bytes.
serve_media = cache_control(max_age=60 * 60 * 24 * 365, immutable=True)(serve_static)

urlpatterns += [
    re_path(
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
        serve_media,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
