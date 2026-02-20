import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_expense():

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jashwanth@18",
        database="financial_analysis"
    )

    cursor = db.cursor()

    cursor.execute("SELECT date, amount FROM expenses")
    data = cursor.fetchall()

    if len(data) < 2:
        return 0

    df = pd.DataFrame(data, columns=["date", "amount"])
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.day

    X = df[["day"]]
    y = df["amount"]

    model = LinearRegression()
    model.fit(X, y)

    next_day = [[30]]
    prediction = model.predict(next_day)

    return round(prediction[0], 2)
