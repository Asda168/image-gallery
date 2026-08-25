from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as serve_static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls')),
]

# django.conf.urls.static.static() is a no-op unless DEBUG=True, so it can't
# be used here: on Vercel DEBUG is off but the media/ dir still ships as part
# of the deployment bundle and needs to be served directly by the app.
urlpatterns += [
    re_path(
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
        serve_static,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
