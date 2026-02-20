import mysql.connector
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

def detect_risk():

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jashwanth@18",
        database="financial_analysis"
    )

    cursor = db.cursor()

    cursor.execute("SELECT amount FROM expenses")
    data = cursor.fetchall()

    if len(data) < 5:
        return "Low Risk"

    df = pd.DataFrame(data, columns=["amount"])

    df["risk"] = df["amount"].apply(lambda x: 1 if x > 5000 else 0)

    X = df[["amount"]]
    y = df["risk"]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    prediction = model.predict([[6000]])

    return "High Risk" if prediction[0] == 1 else "Low Risk"
