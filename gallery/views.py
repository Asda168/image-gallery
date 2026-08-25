from django.contrib import messages
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PhotoUploadForm
from .models import Category, Photo


def gallery_home(request):
    photos = Photo.objects.select_related("category").all()
    categories = Category.objects.all()

    active_slug = request.GET.get("category")
    if active_slug:
        photos = photos.filter(category__slug=active_slug)

    query = request.GET.get("q")
    if query:
        photos = photos.filter(title__icontains=query)

    featured = Photo.objects.filter(is_featured=True).order_by("-uploaded_at")[:5]

    context = {
        "photos": photos,
        "categories": categories,
        "active_slug": active_slug,
        "query": query or "",
        "featured": featured,
        "total_count": photos.count(),
    }
    return render(request, "gallery/home.html", context)


def photo_detail(request, slug):
    photo = get_object_or_404(Photo.objects.select_related("category"), slug=slug)
    related = (
        Photo.objects.filter(category=photo.category)
        .exclude(pk=photo.pk)[:6]
        if photo.category
        else Photo.objects.exclude(pk=photo.pk)[:6]
    )
    return render(request, "gallery/detail.html", {"photo": photo, "related": related})


def upload_photo(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            messages.success(request, "Your photo has been added to the gallery.")
            return redirect(photo.get_absolute_url())
    else:
        form = PhotoUploadForm()
    return render(request, "gallery/upload.html", {"form": form})


@require_POST
def like_photo(request, slug):
    photo = get_object_or_404(Photo, slug=slug)
    Photo.objects.filter(pk=photo.pk).update(likes=F("likes") + 1)
    photo.refresh_from_db()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"likes": photo.likes})
    return redirect(photo.get_absolute_url())
