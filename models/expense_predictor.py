import numpy as np
from sklearn.linear_model import LinearRegression


def predict_expense(amounts):

    if len(amounts) < 2:
        return 0

    X = np.array(range(len(amounts))).reshape(-1, 1)
    y = np.array(amounts)

    model = LinearRegression()
    model.fit(X, y)

    next_index = np.array([[len(amounts)]])

    prediction = model.predict(next_index)

    return round(float(prediction[0]), 2)
