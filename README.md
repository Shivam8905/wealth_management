# 📈 **Wealth Management System**

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


---

## 🔥 **API Endpoints For Postman Testing**

### **Create a BUY Transaction**  
**Method:** POST  

**URL:** `http://127.0.0.1:8000/api/transactions/`  

**Body:**  

{ 
    "company": "Apple Tech", 
    "date": "2025-01-01", 
    "trade_type": 1, 
    "quantity": 100, 
    "price_per_share": 100.0 
}


**Expected Response:**  

{
    "id": 8,
    "company": "Apple Tech",
    "date": "2025-01-01",
    "trade_type": 1,
    "quantity": 100,
    "price_per_share": "100.000",
    "split_ratio": null
}


---

### **Create a SELL Transaction (Partial)**  
**Method:** POST  

**URL:** `http://127.0.0.1:8000/api/transactions/`  

**Body:**  

{
    "company": "Apple Tech",
    "date": "2025-01-02",
    "trade_type": 2,
    "quantity": 50
}

**Expected Response:**  

{
    "id": 9,
    "company": "Apple Tech",
    "date": "2025-01-02",
    "trade_type": 2,
    "quantity": 50,
    "price_per_share": null,
    "split_ratio": null
}


---


### **Create a SPLIT Transaction**  
**Method:** POST  

**URL:** `http://127.0.0.1:8000/api/transactions/`  

**Body:**  

{
    "company": "Apple Tech",
    "date": "2025-01-03",
    "trade_type": 3,
    "split_ratio": "1:2"
}

**Expected Response:**  

{
    "id": 10,
    "company": "Apple Tech",
    "date": "2025-01-03",
    "trade_type": 3,
    "quantity": null,
    "price_per_share": null,
    "split_ratio": "1:2"
}


---


### **Get Average Price and Balance**  
**Method:** GET  

**URL:** `http://127.0.0.1:8000/api/transactions/average-price/?company=Apple Tech`  


**Expected Response:**  

{
    "company": "Apple Tech",
    "average_price": 50.0,
    "balance_quantity": 100
}


---


### **Attempt to Sell More Than Available (Error Handling)**  
**Method:** POST  

**URL:** `http://127.0.0.1:8000/api/transactions/`  

**Body:**  

{
    "company": "Apple Tech",
    "date": "2025-01-04",
    "trade_type": 2,
    "quantity": 10000
}

**Expected Response:** 
400 Bad Request

{
    "Check Stock": [
        "Sell quantity exceeds available holdings Or you don't have stock of this company"
    ]
}


---


### **Create Invalid Split Transaction**  
**Method:** POST  

**URL:** `http://127.0.0.1:8000/api/transactions/`  

**Body:**  

{
    "company": "Apple Tech",
    "date": "2025-01-05",
    "trade_type": 3,
    "split_ratio": "2"
}

**Expected Response:**  
400 Bad Request

{
    "Check Payload": [
        "Invalid split ratio format. Use format like '1:5'"
    ]
}

---
