import mysql.connector

def get_advice():

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jashwanth@18",
        database="financial_analysis"
    )

    cursor = db.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)
    data = cursor.fetchall()

    if not data:
        return "No spending data available."

    highest = max(data, key=lambda x: x[1])

    category = highest[0]
    amount = highest[1]

    if amount > 7000:
        return f"You are spending too much on {category}. Try reducing by 10-15%."

    else:
        return "Your spending looks balanced. Keep saving consistently!"
