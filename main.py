from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_connection():

    conn = mysql.connector.connect(
        host=os.getenv("Host"),
        user=os.getenv("User"),
        password=os.getenv("Password"),
        database=os.getenv("Database_name"),
        port=int(os.getenv("Port"))
    )

    return conn


conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    amount FLOAT,
    category VARCHAR(100),
    payment_method VARCHAR(100),
    expense_date DATE,
    description TEXT
)
""")

conn.commit()

cursor.close()
conn.close()


@app.get("/")
def home():

    return {
        "message": "API Running Successfully"
    }


@app.post("/add_expense")
def add_expense(payload: dict):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO expenses
    (title, amount, category, payment_method, expense_date, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        payload["title"],
        payload["amount"],
        payload["category"],
        payload["payment_method"],
        payload["expense_date"],
        payload["description"]
    )

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Expense Added Successfully"
    }


@app.get("/get_expenses")
def get_expenses():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT *
    FROM expenses
    ORDER BY expense_id DESC
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "expenses": data
    }