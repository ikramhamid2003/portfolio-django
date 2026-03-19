#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

---

## Step 3 — Create a `.gitignore` file

Create `D:\portfolioDjango\.gitignore`:
```
venv/
__pycache__/
*.pyc
db.sqlite3
media/
staticfiles/
.env