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

## Add photos from media/photos/

Drop image files directly into `media/photos/`, then run:

```bash
python manage.py import_photos
```

Any image file sitting there that isn't already in the database gets registered as a new `Photo` (add category/title/etc. afterwards from the admin panel if needed).

## Uploading via the website

The "Upload" button in the header opens a form to add a photo straight from the browser. Note: on Vercel the deployed filesystem is read-only, so uploads there will fail — this only works reliably when running locally (or once a durable storage backend like Vercel Blob or S3 is wired up).

## Structure

- `gallery/` — the app: models (`Category`, `Photo`), views, forms, admin, templates, static assets
- `gallery_site/` — Django project settings/urls
- `media/` — gallery images (`media/photos/`)
