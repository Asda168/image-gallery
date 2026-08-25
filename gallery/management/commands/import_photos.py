import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from gallery.models import Photo

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
TIMESTAMP_SUFFIX = re.compile(r"_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$")


class Command(BaseCommand):
    help = "Register image files sitting directly in media/photos/ that aren't in the database yet."

    def handle(self, *args, **options):
        photos_dir = Path(settings.MEDIA_ROOT) / "photos"
        if not photos_dir.is_dir():
            self.stdout.write(self.style.WARNING(f"{photos_dir} does not exist."))
            return

        existing = set(Photo.objects.values_list("image", flat=True))

        created = 0
        for path in sorted(photos_dir.iterdir()):
            if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
                continue

            rel_name = f"photos/{path.name}"
            if rel_name in existing:
                continue

            title = TIMESTAMP_SUFFIX.sub("", path.stem)
            title = title.replace("_", " ").replace("-", " ").strip().title()

            photo = Photo(title=title or path.stem)
            photo.image.name = rel_name
            photo.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Registered {created} new photo(s) from media/photos/."))
