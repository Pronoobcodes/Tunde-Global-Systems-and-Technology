# Tunde Global Systems and Technology

This is a Django-based e-commerce demo for Tunde Global Systems and Technology. It includes a simple product catalog, cart, and a WhatsApp-based checkout flow.

## Features
- Product listing and detail pages
- Shopping cart with quantity updates and remove/clear actions
- WhatsApp checkout: pressing "Proceed to Checkout" opens WhatsApp with a prefilled order message including customer name, address, products and totals

## Local setup

Requirements
- Python 3.8+
- A virtual environment (recommended)

Install and run

```powershell
cd 'c:\Users\USER\Tunde-Global-Systems-and-Technology'
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt  
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## WhatsApp Checkout
When a user clicks "Proceed to Checkout" on the cart page, the site builds a message containing:
- Customer name and address (prompts guest users)
- The list of products in the cart with quantities and line totals
- Order total

This message is opened in WhatsApp using the merchant number `+234 812 748 4707`.

If you'd like a different merchant phone, update the number in `cart/templates/cart/cart_summary.html` (variable `merchantPhone`).

## Next steps
- Add a logo asset and polish navbar
- Add server-side order persistence and confirmation flow
- Improve UX for guests (collect name/address during checkout form instead of JS prompts)

---
Generated changes:
- Added `static/css/custom.css` (visual improvements)
- Updated several store templates to use refreshed styles
- Implemented WhatsApp checkout redirect in `cart_summary.html`
# Tunde Global Systems and Technology

This is a small Django-based e-commerce demo application used for showcasing products and a lightweight cart system.

## Quick overview
- Django project with apps: `store`, `cart`, `custom_auth`.
- Uses Bootstrap 5 for layout and has custom styles in `static/css/custom.css`.

## Requirements
- Python 3.8+ (use your preferred environment manager)
- Django (version used by the project)

## Setup (development)
1. Create and activate a virtual environment:

```powershell
cd 'c:\Users\USER\Tunde-Global-Systems-and-Technology'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (if you have `requirements.txt`):

```powershell
pip install -r requirements.txt
```

3. Run migrations and start the dev server:

```powershell
python manage.py migrate
python manage.py runserver
```

4. Open the site in your browser at `http://127.0.0.1:8000/`.

## Static files
During development Django serves static files automatically when `DEBUG=True`. For production, collect static files:

```powershell
python manage.py collectstatic
```

## What I changed recently
- Added `static/css/custom.css` for improved frontend styles.
- Updated several templates under `store/templates/store/` to improve layout and navbar branding.
- Fixed the cart count to use the `cart` context processor.

## Next suggestions
- Add a logo to `static/assets/` and reference it in the navbar.
- Add minor JS interactivity (mobile menu toggle, small animations).

