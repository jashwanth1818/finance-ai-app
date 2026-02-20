# models/advisor.py

def give_advice(categories, amounts):
    advice = []

    try:
        for i in range(len(categories)):
            if float(amounts[i]) > 5000:
                advice.append(f"High spending detected in {categories[i]}")
    except:
        pass

    if not advice:
        advice.append("Your spending is under control")

    return advice