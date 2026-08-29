from django.contrib import messages
from django.db.models import F, Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PhotoUploadForm
from .models import Category, Photo


def _has_image_file(photo):
    return bool(photo.image) and photo.image.storage.exists(photo.image.name)


def _only_existing(queryset):
    return [p for p in queryset if _has_image_file(p)]


def gallery_home(request):
    photos_qs = Photo.objects.select_related("category").exclude(image="")
    categories = Category.objects.all()

    active_slug = request.GET.get("category")
    if active_slug:
        photos_qs = photos_qs.filter(category__slug=active_slug)

    query = request.GET.get("q")
    if query:
        photos_qs = photos_qs.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(photographer__icontains=query)
        )

    photos = _only_existing(photos_qs)
    featured = _only_existing(
        Photo.objects.filter(is_featured=True).exclude(image="").order_by("-uploaded_at")[:10]
    )[:3]

    context = {
        "photos": photos,
        "categories": categories,
        "active_slug": active_slug,
        "query": query or "",
        "featured": featured,
        "total_count": len(photos),
        "all_count": len(_only_existing(Photo.objects.exclude(image=""))),
    }
    return render(request, "gallery/home.html", context)


def photo_detail(request, slug):
    photo = get_object_or_404(Photo.objects.select_related("category"), slug=slug)
    if not _has_image_file(photo):
        raise Http404("This photo's image file is missing.")

    related_qs = Photo.objects.exclude(image="").exclude(pk=photo.pk)
    if photo.category:
        related_qs = related_qs.filter(category=photo.category)
    related = _only_existing(related_qs[:12])[:6]

    return render(request, "gallery/detail.html", {"photo": photo, "related": related})


def upload_photo(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist(form.add_prefix("image"))
        if form.is_valid():
            photo = form.save(commit=False)
            extra_files = files[1:]
            photo.save()
            for i, extra in enumerate(extra_files, start=2):
                Photo.objects.create(
                    title=f"{form.cleaned_data['title']} {i}",
                    description=form.cleaned_data["description"],
                    image=extra,
                    category=form.cleaned_data["category"],
                    photographer=form.cleaned_data["photographer"],
                )
            count = 1 + len(extra_files)
            messages.success(
                request,
                "Your photo has been added to the gallery."
                if count == 1
                else f"{count} photos have been added to the gallery.",
            )
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
