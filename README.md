# HBIBWASH - Car Wash Booking App

A Django-based booking system for a car wash business.

## Project Structure

```
carwash_project/
|-- carwash/            # Project settings & URLs
|-- accounts/           # Login and user roles
|-- bookings/           # Booking logic, status management
|-- services/           # Service catalog + home page
|-- dashboard/          # Admin panel (staff only)
|-- templates/          # All HTML pages
|   |-- base.html
|   |-- home/
|   |-- accounts/
|   |-- bookings/
|   |-- services/
|   `-- dashboard/
|-- static/             # CSS, JS, images
|-- manage.py
`-- requirements.txt
```

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Create a superuser (owner/admin account)
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Then open http://127.0.0.1:8000

## Pages

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/services/` | Services list |
| `/bookings/new/` | Create a booking |
| `/accounts/login/` | Admin login |
| `/dashboard/` | Owner dashboard (staff only) |
| `/dashboard/bookings/` | Manage all bookings |
| `/dashboard/services/` | Add/edit/hide services |

## User Roles

- **Public visitor** - browses services and books appointments without an account
- **Staff/Owner** - logs in to access the `/dashboard/` panel

To make a user staff: Django Admin > Users > tick "Staff status"

## Customization

- Change business name: search `HBIBWASH` in templates
- Change currency: search `DT` in templates
- Change location/phone: `templates/bookings/create.html` sidebar
- Add services: via `/dashboard/services/` after login as staff
