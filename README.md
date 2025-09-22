# Django Expense Tracker

A web application that helps users **track and manage their expenses**.  
The project is built with the Django framework and organized into two main apps:

- **public** – handles all public-facing pages (landing, registration, login).
- **expenses** – handles the internal, authenticated features for tracking expenses.

---

## 🚀 Features (Current & Planned)
### Public (Unauthenticated)
- Landing page with quick introduction
- User registration
- User login & logout

### Private (Authenticated)
- Add, edit, and delete expenses
- View expense history
- Categorize expenses (e.g., Food, Transport)
- Dashboard with total spending summary
- (Planned) Charts & reports
- (Planned) Budget goals & savings tracker

---

## 🛠️ Tech Stack
- **Backend:** [Django](https://www.djangoproject.com/) 5.x (Python 3.x)
- **Database:** SQLite (default) → can switch to PostgreSQL/MySQL later
- **Frontend:** Django Templates, HTML5, CSS3, Bootstrap/Tailwind (your choice)
- **Version Control:** Git & GitHub

---

## 📂 Project Structure
django-expense-tracker/ ├─ README.md ├─ manage.py ├─ expensetracker/       # Django project settings & configuration ├─ public/               # Landing, registration, login (outside pages) └─ expenses/             # Core expense tracking logic (inside pages)


---

## ⚡ Quick Start
```bash
# 1️⃣ Clone repository
git clone https://github.com/<your-username>/django-expense-tracker.git
cd django-expense-tracker

# 2️⃣ (Optional) Create & activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install django

# 4️⃣ Run migrations
python manage.py migrate

# 5️⃣ Start the development server
python manage.py runserver
