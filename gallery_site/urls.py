from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls')),
]

# Served unconditionally (not just in DEBUG) so the committed seed photos
# are reachable on Vercel too, where DEBUG is off but the media/ dir still
# ships as part of the deployment bundle.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
