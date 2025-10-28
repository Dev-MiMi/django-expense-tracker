Perfect 👍 — let’s extend your README.md so it documents the public app’s files (registration, login, password reset, JWT, etc.) and their purpose, along with the API endpoints for the DRF parts.

Here’s a clean, professional updated version you can safely replace your current README.md with 👇


---

# 💰 Django Expense Tracker

A complete **Expense Tracking and Budget Management** web application built with Django.  
It supports both **web-based pages (forms + templates)** and a **REST API (DRF)** for integration or frontend frameworks like React.

---

## 🚀 Features

### 🧍‍♂️ Public (Unauthenticated)
- Landing page with app overview
- User registration and login (Django forms)
- JWT-based API authentication (DRF)
- Password reset via email link

### 🔒 Private (Authenticated)
- Create, edit, and delete accounts and expense records
- Categorize expenses (e.g., Food, Transport)
- Budget creation and tracking with progress calculation
- Multi-account and multi-currency support
- View spending history by category or period
- (Planned) Charts & insights dashboard

---

## 🧠 Tech Stack
| Layer | Technology |
|-------|-------------|
| **Backend** | Django 5.x, Django REST Framework (DRF) |
| **Database** | SQLite (default), supports PostgreSQL/MySQL |
| **Auth** | Django session auth & JWT (SimpleJWT) |
| **Frontend** | Django Templates (HTML5, CSS3, Bootstrap/Tailwind) |
| **Version Control** | Git & GitHub |

---

## 🧩 Project Structure

django-expense-tracker/ ├── manage.py ├── README.md ├── expensetracker/              # Project config (settings, urls, wsgi) │ ├── public/                      # Handles public views & auth │   ├── models.py                # User-related models (if extended) │   ├── views.py                 # Registration & login views │   ├── views_api.py             # API views (registration, profile, etc.) │   ├── views_jwt.py             # JWT login/refresh endpoints │   ├── views_password_reset.py  # Email-based password reset logic │   ├── forms.py                 # Django forms for registration/login │   ├── jwt_serializers.py       # Custom JWT serializer │   ├── serializers.py           # General serializers │   ├── serializers_password_reset.py # Password reset serializers │   ├── urls.py                  # Template-based routes │   ├── api_urls.py              # DRF API routes │   ├── templates/               # HTML templates (login, signup, reset, etc.) │   ├── static/                  # CSS, JS, images │   └── tests.py │ └── private/                     # Authenticated user app ├── models.py                # Account, Record, Budget models ├── serializers.py           # DRF serializers ├── views.py                 # Django views (if any) ├── views_api.py             # DRF API endpoints ├── urls.py                  # Template routes ├── api_urls.py              # DRF API routes ├── templates/               # Dashboard & expense pages └── tests.py

---

## ⚙️ API Endpoints

### 🔑 Authentication (JWT)
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/api/register/` | Create new user |
| `POST` | `/api/token/` | Obtain access and refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh access token |
| `POST` | `/api/password-reset/` | Send password reset link |
| `POST` | `/api/password-reset/confirm/` | Confirm reset using token |

---

### 💵 Private API (Authenticated)
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/api/accounts/` | List user accounts |
| `POST` | `/api/accounts/` | Create new account |
| `GET` | `/api/records/` | View all expense records |
| `POST` | `/api/records/` | Add new record |
| `GET` | `/api/budgets/` | View user budgets |
| `POST` | `/api/budgets/` | Create new budget |
| `PUT`/`PATCH` | `/api/budgets/<id>/` | Update a budget |
| `DELETE` | `/api/budgets/<id>/` | Delete a budget |

> 🧠 All authenticated endpoints require:
> ```
> Authorization: Bearer <your_access_token>
> ```

---

## 🧾 Example: Create a Budget (cURL)

```bash
curl -X POST http://127.0.0.1:8000/api/budgets/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Monthly Budget",
        "categories": ["Food & Drinks", "Groceries"],
        "period": "Month",
        "start_date": "2025-10-01",
        "end_date": "2025-10-31",
        "amount": "2000.00",
        "currency": "USD",
        "account": [1]
      }'


---

🧰 Setup Instructions

# Clone repository
git clone https://github.com/<your-username>/django-expense-tracker.git
cd django-expense-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver


---

📊 Future Enhancements

Charts (using Chart.js or Recharts)

AI-powered spending suggestions

Multi-currency conversion

Export reports (CSV/PDF)

React or Next.js frontend for the API



---

🧑‍💻 Author

Miracle Olagundoye
Built with ❤️ using Django & DRF.

---


