# Wealth Management System

A Django-based stock transaction management system that allows users to **BUY**, **SELL**, and **SPLIT** stock transactions. The system also calculates the **average price** and **remaining stock balance** after each transaction using FIFO (First In, First Out) logic.

---

## 🚀 **Features**
✅ Handle `BUY`, `SELL`, and `SPLIT` stock transactions  
✅ FIFO-based transaction handling  
✅ Average price calculation  
✅ Edge case handling (insufficient stocks, invalid splits)  
✅ RESTful API using Django REST Framework  

---

## 🏗️ **Project Setup**
### ✅ **Follow These Steps to Set Up the Project**  
```bash
# Clone the repository
git clone https://github.com/Shivam8905/wealth_management.git
cd wealth_management

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start the development server
python manage.py runserver
