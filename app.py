from flask import Flask, render_template, request, redirect
import mysql.connector
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from models.expense_predictor import predict_expense
from models.risk_detector import detect_risk
from models.advisor import give_advice

app = Flask(__name__)

# 🔵 Railway DB Connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )

# 🟢 Dashboard
@app.route('/')
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE type='income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE type='expense'")
    expense = cursor.fetchone()[0] or 0

    savings = income - expense

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE type='expense'
        GROUP BY category
    """)
    data = cursor.fetchall()

    categories = [row[0] for row in data]
    values = [float(row[1]) for row in data]

    # 📊 Chart
    if values:
        plt.figure()
        plt.pie(values, labels=categories, autopct='%1.1f%%')
        plt.title("Expense Distribution")
        plt.savefig('static/chart.png')
        plt.close()

    # 🤖 AI Prediction
    cursor.execute("SELECT amount FROM expenses WHERE type='expense'")
    db_data = cursor.fetchall()

    amounts = [float(row[0]) for row in db_data]

    if len(amounts) > 2:
        prediction = predict_expense(amounts)
        risk = detect_risk(amounts)
        advice = give_advice(income, expense)
    else:
        prediction = 0
        risk = "Add more expenses"
        advice = "Track spending to get advice"

    conn.close()

    return render_template("dashboard.html",
                           income=income,
                           expense=expense,
                           savings=savings,
                           prediction=prediction,
                           risk=risk,
                           advice=advice)

# 🟢 Add Expense Page
@app.route('/add', methods=['GET','POST'])
def add_expense():

    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        type_ = request.form['type']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO expenses (amount,category,type) VALUES (%s,%s,%s)",
            (amount,category,type_)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')

    return render_template("add_expense.html")

# 🔴 Render Port Fix
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))

