def give_advice(categories, amounts):

    advice = []

    for i in range(len(categories)):
        if amounts[i] > 5000:
            advice.append(f"High spending detected in {categories[i]}")

    if not advice:
        advice.append("Your spending is under control")

    return advice
