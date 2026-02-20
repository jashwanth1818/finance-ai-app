from flask import Flask, render_template, request, redirect
import mysql.connector
import os
import matplotlib
import models.advisor as advisor
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from models.expense_predictor import predict_expense
from models.risk_detector import detect_risk


app = Flask(__name__)

# ================= DATABASE CONNECTION =================
from urllib.parse import urlparse
import os
import mysql.connector

def get_connection():
    db_url = os.getenv("DATABASE_URL")

    url = urlparse(db_url)

    return mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path.replace("/", ""),
        port=url.port if url.port else 3306   # ⭐ FINAL FIX
    )

# ================= DASHBOARD =================

@app.route('/')
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE type='income'")
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE type='expense'")
    total_expense = cursor.fetchone()[0] or 0

    savings = total_income - total_expense

    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE type='expense' GROUP BY category")
    category_data = cursor.fetchall()

    categories = [x[0] for x in category_data]
    amounts = [float(x[1]) for x in category_data]

    # CHART
    if len(categories) > 0:
        plt.figure()
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        chart_path = os.path.join('static', 'chart.png')
        plt.savefig(chart_path)
        plt.close()

    prediction = predict_expense(amounts)
    risk = detect_risk(total_income, total_expense)
    advice = advisor.give_advice(categories, amounts)
    conn.close()

    return render_template(
        "dashboard.html",
        income=total_income,
        expense=total_expense,
        savings=savings,
        breakdown=category_data,
        prediction=prediction,
        risk=risk,
        advice=advice
    )

# ================= ADD EXPENSE =================

@app.route('/add', methods=['GET','POST'])
def add_expense():

    if request.method == 'POST':

        amount = request.form['amount']
        category = request.form['category']
        type_ = request.form['type']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO expenses(amount,category,type) VALUES(%s,%s,%s)",
            (amount,category,type_)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("add_expense.html")

# ================= RENDER PORT FIX =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

