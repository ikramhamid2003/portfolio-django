# Ikram Hamid P K — Portfolio Website

Full-stack portfolio built with **Django 4.2**, **Tailwind CSS CDN**, and **Neon PostgreSQL**.

## Features
- Fully responsive (mobile, tablet, desktop)
- Scroll-reveal animations + animated hamburger nav
- Project cards, experience timeline, skills, certifications
- AJAX contact form with toast notifications
- **Analytics dashboard** (admin-only, protected login)
  - Visitor tracking: IP, country, city, device, browser, OS
  - Time-on-site tracking (beacon on tab close)
  - Daily visitor chart (Chart.js)
  - Device donut chart
  - Top countries, browsers, OS tables
  - Recent 50 visitors detail table
  - Contact messages inbox

## Quick Start

### Windows (PowerShell)
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser   # one-time
.\setup.ps1
```

### Manual
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
cp .env.example .env         # then fill in your values
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

## Neon PostgreSQL Setup
1. Go to https://console.neon.tech and create a free account
2. Create a new project → copy the **Connection string**
3. Paste it as `DATABASE_URL` in your `.env` file
4. Run `python manage.py migrate`

## Environment Variables (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

## URLs
| URL | Description |
|-----|-------------|
| `/` | Portfolio (public) |
| `/admin/` | Django admin panel |
| `/analytics/login/` | Analytics login (admin only) |
| `/analytics/` | Analytics dashboard (requires login) |

## Deployment (Render)
1. Add to `ALLOWED_HOSTS` in `.env`: your render domain
2. Set `DEBUG=False`
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
4. Start command: `gunicorn portfolio_site.wsgi`
5. Set all env vars in Render dashboard
