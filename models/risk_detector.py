import os
import mysql.connector
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from urllib.parse import urlparse


def get_connection():

    db_url = os.getenv("MYSQL_URL")

    url = urlparse(db_url)

    return mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path.replace('/', ''),
        port=url.port
    )


def detect_risk():

    db = get_connection()
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

    if prediction[0] == 1:
        return "High Risk"
    else:
        return "Low Risk"