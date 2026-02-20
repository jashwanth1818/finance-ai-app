from sklearn.linear_model import LinearRegression
import numpy as np

def predict_expense(amounts):

    if len(amounts) < 2:
        return 0

    X = np.array(range(len(amounts))).reshape(-1,1)
    y = np.array(amounts)

    model = LinearRegression()
    model.fit(X,y)

    next_month = model.predict([[len(amounts)]])
    
    return round(float(next_month[0]),2)
