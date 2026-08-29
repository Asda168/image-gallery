import io

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

THUMBNAIL_LONG_EDGE = 640
THUMBNAIL_QUALITY = 72


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="photos/%Y/%m/")
    thumbnail = models.ImageField(upload_to="thumbnails/%Y/%m/", blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="photos"
    )
    photographer = models.CharField(max_length=80, blank=True)
    is_featured = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 1
            while Photo.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug

        regenerate_thumb = self.image and not self.thumbnail
        super().save(*args, **kwargs)
        if regenerate_thumb:
            self._generate_thumbnail()

    def _generate_thumbnail(self):
        from PIL import Image, ImageOps

        self.image.open()
        try:
            img = Image.open(self.image)
            img.load()
            img = ImageOps.exif_transpose(img)
        finally:
            self.image.close()

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        w, h = img.size
        if max(w, h) > THUMBNAIL_LONG_EDGE:
            scale = THUMBNAIL_LONG_EDGE / max(w, h)
            img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, "JPEG", quality=THUMBNAIL_QUALITY, optimize=True)
        name = self.image.name.rsplit("/", 1)[-1].rsplit(".", 1)[0] + ".jpg"
        self.thumbnail.save(name, ContentFile(buffer.getvalue()), save=False)
        Photo.objects.filter(pk=self.pk).update(thumbnail=self.thumbnail.name)

    @property
    def thumb_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return self.image.url

    def get_absolute_url(self):
        return reverse("gallery:photo_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title
