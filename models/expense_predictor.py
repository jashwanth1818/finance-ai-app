import numpy as np
from sklearn.linear_model import LinearRegression

def predict_expense(amounts):

    if len(amounts) == 0:
        return 0

    X = np.array(range(len(amounts))).reshape(-1, 1)
    y = np.array(amounts)

    model = LinearRegression()
    model.fit(X, y)

    next_month = np.array([[len(amounts)]])
    prediction = model.predict(next_month)

    return round(prediction[0], 2)
