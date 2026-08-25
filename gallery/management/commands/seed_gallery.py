import io
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFilter

from gallery.models import Category, Photo

CATEGORIES = ["Nature", "Architecture", "Portrait", "Street", "Abstract", "Travel"]

PHOTOS = [
    ("Golden Hour Ridge", "Nature", "A sweeping mountain ridge lit by the last light of day."),
    ("Glass Tower", "Architecture", "Reflections layered across a downtown high-rise."),
    ("Quiet Gaze", "Portrait", "A candid portrait caught between two thoughts."),
    ("Rainy Crossing", "Street", "Umbrellas and neon on a wet city street."),
    ("Fluid Forms", "Abstract", "Color and motion blurred into something new."),
    ("Coastal Drift", "Travel", "A lone boat drifting along a quiet coastline."),
    ("Forest Light", "Nature", "Sunbeams cutting through an old growth forest."),
    ("Concrete Lines", "Architecture", "Brutalist geometry against a pale sky."),
    ("Market Morning", "Street", "Early light over a bustling market stall."),
    ("Study in Blue", "Abstract", "A minimal composition built from shades of blue."),
    ("Desert Road", "Travel", "An empty highway vanishing into heat haze."),
    ("Still Water", "Nature", "A mirror-calm lake at first light."),
    ("City Grid", "Architecture", "Windows repeating into an urban pattern."),
    ("Passing Glance", "Portrait", "A fleeting expression caught mid-stride."),
    ("Night Market", "Street", "Lantern light spilling over a night bazaar."),
    ("Warm Noise", "Abstract", "Grain and gradient layered like static light."),
]

PALETTES = [
    ((20, 24, 38), (232, 185, 106)),
    ((30, 18, 30), (232, 116, 138)),
    ((14, 30, 26), (120, 200, 170)),
    ((26, 20, 40), (170, 140, 230)),
    ((32, 24, 16), (240, 170, 90)),
    ((16, 26, 34), (110, 180, 220)),
]


def make_image(seed_text, size):
    w, h = size
    palette = random.choice(PALETTES)
    base = Image.new("RGB", (w, h), palette[0])
    draw = ImageDraw.Draw(base)

    for i in range(0, w + h, 14):
        shade = tuple(min(255, c + random.randint(-6, 20)) for c in palette[0])
        draw.line([(i, 0), (0, i)], fill=shade, width=6)

    glow = Image.new("RGB", (w, h), (0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    cx, cy = random.randint(0, w), random.randint(0, h)
    gdraw.ellipse(
        [cx - w * 0.5, cy - h * 0.5, cx + w * 0.5, cy + h * 0.5], fill=palette[1]
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=min(w, h) // 3))
    base = Image.blend(base, glow, alpha=0.35)

    buf = io.BytesIO()
    base.save(buf, format="JPEG", quality=87)
    return ContentFile(buf.getvalue(), name=f"{seed_text}.jpg")


class Command(BaseCommand):
    help = "Seed the gallery with categories and generated placeholder photos."

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true", help="Delete existing photos/categories first.")

    def handle(self, *args, **options):
        if options["flush"]:
            Photo.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write("Cleared existing gallery data.")

        categories = {}
        for name in CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name)
            categories[name] = cat

        aspect_ratios = [(800, 1000), (900, 700), (800, 1200), (900, 900), (1000, 650)]

        created = 0
        for title, cat_name, description in PHOTOS:
            if Photo.objects.filter(title=title).exists():
                continue
            size = random.choice(aspect_ratios)
            image_file = make_image(title.lower().replace(" ", "-"), size)
            photo = Photo(
                title=title,
                description=description,
                category=categories[cat_name],
                photographer=random.choice(["A. Rivera", "J. Chen", "M. Okafor", "S. Larsen", ""]),
                is_featured=random.random() < 0.3,
                likes=random.randint(0, 340),
            )
            photo.image.save(image_file.name, image_file, save=False)
            photo.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} photos across {len(CATEGORIES)} categories."))
