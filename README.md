# 🛡️ Secure Vault

## What is this?

In today's digital world, the average person has 80+ online accounts but uses only 5-7 different passwords. This creates a massive security risk - if one account gets hacked, all your accounts are compromised.

Secure Vault solves this problem by providing a secure place to store unique passwords for every account, plus tools to generate strong passwords and monitor your overall security health.

## Features

- **🔐 Password Vault** - Secure storage for all your passwords with encryption
- **🎲 Password Generator** - Create strong, unique passwords instantly  
- **📊 Activity Logs** - Track all vault activities and access history
- **🔍 Security Audits** - Regular security checks and vulnerability assessments
- **🎨 Modern UI** - Clean, responsive interface built with Bootstrap

## Live Demo
**Try it now:** [https://secure-vault-v489.onrender.com](https://secure-vault-v489.onrender.com)

## Local Development

Want to run it locally? Here's how:

1. **Clone the repository**
   ```bash
   git clone https://github.com/PetarValev/secure-vault
   cd secure-vault
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows:
   venv\Scripts\activate
   
   # Linux/Mac:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Database Setup**
   
   **Option A: PostgreSQL (Recommended)**
   - Create `.env` file with database credentials:
     ```
     DB_NAME=your_db_name
     DB_USER=your_username
     DB_PASSWORD=your_password
     DB_HOST=localhost
     DB_PORT=5432
     ```

   **Option B: SQLite (Quick Testing)**
   - In `settings.py`, comment out PostgreSQL config
   - Uncomment SQLite configuration for easy local testing

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main app: `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## Tech Stack

- Django 5.2.4
- Python 3.x
- PostgreSQL/SQLite
- Bootstrap 5
- JavaScript
- Deployed on Render