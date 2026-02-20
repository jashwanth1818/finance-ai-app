# models/advisor.py

def give_advice(income, expense):

    if income == 0:
        return "No income data"

    ratio = expense/income

    if ratio > 0.7:
        return "You are spending too much 😟"
    elif ratio > 0.5:
        return "Moderate spending 👍"
    else:
        return "Good savings habit 💰"