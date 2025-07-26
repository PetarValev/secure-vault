# 🛡️ Secure Vault

A secure password management application built with Django. Store and generate passwords safely with a clean, modern interface.

## ✨ Features

- **🔐 Password Vault** - Secure storage for all your passwords with encryption
- **🎲 Password Generator** - Create strong, unique passwords instantly  
- **📊 Activity Logs** - Track all vault activities and access history
- **🔍 Security Audits** - Regular security checks and vulnerability assessments
- **🛡️ Security First** - We can't see your passwords, even if we wanted to
- **🎨 Modern UI** - Clean, responsive interface built with Bootstrap

## Setup Instructions

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