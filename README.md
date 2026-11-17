# Travel Outfit

Travel Outfit is a Django website for browsing travel products, managing customer and supplier accounts, and handling carts, bookings, and feedback. It also includes a weather page.

## Requirements

- Python 3.12 or newer
- Internet access for the weather feature

## Run locally

From the project folder, create and activate a virtual environment, then install the dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install Django requests Pillow
```

Apply the database migrations and start the development server:

```powershell
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. The Django admin is available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/); create an admin account with `python manage.py createsuperuser`.

The project uses SQLite, so migrations create the local database automatically. The weather page uses an external weather service and requires a valid API key.
