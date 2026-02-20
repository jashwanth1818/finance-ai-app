from flask import Flask, render_template, request, redirect, Response
import mysql.connector
import matplotlib.pyplot as plt
import io
import os


from models.expense_predictor import predict_expense
from models.risk_detector import detect_risk
from models.advisor import get_advice

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)



cursor = db.cursor()

# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():

    # Get income
    cursor.execute("SELECT monthly_income FROM users LIMIT 1")
    income_result = cursor.fetchone()
    income = income_result[0] if income_result else 0

    # Total expense
    cursor.execute("SELECT SUM(amount) FROM expenses")
    expense_result = cursor.fetchone()
    total_expense = expense_result[0] if expense_result and expense_result[0] else 0

    savings = income - total_expense
    if income > 0:
        saving_rate = round((savings / income) * 100, 2)
    else:
        saving_rate = 0


    # Category breakdown
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    category_data = cursor.fetchall()

    predicted = predict_expense()
    risk = detect_risk()
    advice = get_advice()

    return render_template(
        "dashboard.html",
        income=income,
        expense=total_expense,
        savings=savings,
        category_data=category_data,
        predicted=predicted,
        risk=risk,
        advice=advice,
        saving_rate=saving_rate,
        warnings=warnings,
        trend=trend

    )
warnings = []

cursor.execute("""
SELECT category, SUM(amount)
FROM expenses
GROUP BY category
""")

expense_data = cursor.fetchall()

cursor.execute("""
SELECT category, monthly_limit
FROM budgets
WHERE user_id = 1
""")

budget_data = cursor.fetchall()

budget_dict = dict(budget_data)

for cat, amt in expense_data:
    if cat in budget_dict and amt > budget_dict[cat]:
        warnings.append(f"{cat} budget exceeded!")


# ---------------- ADD EXPENSE ----------------
@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":
        category = request.form["category"]
        amount = request.form["amount"]
        date = request.form["date"]

        query = """
        INSERT INTO expenses (user_id, category, amount, date)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (1, category, amount, date))
        db.commit()

        return redirect("/?added=1")


    return render_template("add_expense.html")
cursor.execute("""
SELECT SUM(amount)
FROM expenses
WHERE MONTH(date) = MONTH(CURDATE())
""")
this_month = cursor.fetchone()[0] or 0

cursor.execute("""
SELECT SUM(amount)
FROM expenses
WHERE MONTH(date) = MONTH(CURDATE()) - 1
""")
last_month = cursor.fetchone()[0] or 0

if last_month > 0:
    trend = round(((this_month - last_month) / last_month) * 100, 2)
else:
    trend = 0


# ---------------- CHART ROUTE ----------------
@app.route("/chart.png")
def chart():

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    category_data = cursor.fetchall()

    categories = [row[0] for row in category_data]
    amounts = [float(row[1]) for row in category_data]

    plt.figure()
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Expense Distribution")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return Response(img.getvalue(), mimetype='image/png')

# ---------------- RUN APP ----------------


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


