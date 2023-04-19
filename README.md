# Django service practice

An inventory-and-orders exercise built with Django REST Framework. The current code provides basic list/create routes and inventory/taxonomy detail routes. It is a starting point for the eight tasks in [CHALLENGES.md](CHALLENGES.md), not a completed inventory-management product.

## What is here

Inventory records reference a type and language and can carry tags and JSON metadata. Orders and order tags have separate list/create endpoints. Django's standard user model remains in use: the requested custom profile, date filters, deactivation endpoint, tag lookups, three-item pagination, and challenge-eight walkthrough are not completed.

| Route | Current handlers |
| --- | --- |
| `/inventory/` | GET, POST |
| `/inventory/<id>/` | GET, PATCH, DELETE |
| `/inventory/tags/`, `/inventory/types/`, `/inventory/languages/` | GET, POST; detail GET/PATCH/DELETE |
| `/orders/`, `/orders/tags/` | GET, POST |
| `/admin/` | Standard Django admin; challenge-specific registration remains unfinished |

Missing inventory or taxonomy records return 404. List responses are currently unpaginated arrays. These routes retain the exercise's anonymous access, including writes; use a local disposable database. They need an explicit authorization policy before public hosting.

## Local setup

Python 3.11 and PostgreSQL 15 are a practical local starting point. The historical requirements pin Django 4.1 and Pydantic 1; no dependency modernization is included.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill `POSTGRES_PASSWORD` with a private local value. `DEBUG=true` is explicitly local and generates an ephemeral Django key if none is set; configure a stable private `DJANGO_SECRET_KEY` outside that mode. The application loads the root `.env`.

```sh
docker compose --file docker-compose.dev.yml up -d
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

The database is bound to `127.0.0.1:5444` and stored in the `pgdata` volume. Setup scripts install requirements and migrate; they no longer seed automatically. `database.py` is a data-writing sample generator, not an importable application library. Inspect it before optionally running `python manage.py shell -c "import database"` against a disposable database. The sample generator is not guaranteed idempotent and was not executed in this review.

## Checks and boundaries

```sh
python manage.py test --settings=config.settings.test
```

Three tests pass with Django 4.2 and an in-memory SQLite database: empty inventory, empty order routes, and twelve missing-record operations across inventory/taxonomy endpoints. All Python files parse. PostgreSQL, the historical pinned environment, seed execution, and setup scripts were not run. SQLite tests do not establish PostgreSQL parity.

Creation of inventory still uses nested read serializers without implemented nested writes. Its Pydantic metadata includes a Decimal rating, which also requires deliberate JSON conversion before persistence; the create path is unfinished. PATCH does not apply the same metadata schema as POST. These are concrete remaining challenge work, rather than working features to advertise. No UI is present; endpoint tables and real test results are more useful here than a screenshot.
