# Nisa Gallery — Django Image Gallery

A dark, elegant photo gallery built with Django: masonry grid, category filters, search, live like button, and a drag-and-drop upload page.

## Run it

```bash
.venv\Scripts\activate
python manage.py runserver
```

Visit http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/ — login `admin` / `admin12345` (change this before any real deployment).

## Re-seed sample photos

```bash
python manage.py seed_gallery --flush
```

Generates placeholder photos with Pillow so the gallery looks populated without needing external images.

## Structure

- `gallery/` — the app: models (`Category`, `Photo`), views, forms, admin, templates, static assets
- `gallery_site/` — Django project settings/urls
- `media/` — uploaded images (created at runtime)
