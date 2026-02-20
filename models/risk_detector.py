

def detect_risk(amounts):

    if not amounts:
        return "No Data"

    avg = sum(amounts) / len(amounts)

    if avg > 5000:
        return "High Risk Spending ⚠️"
    else:
        return "Low Risk Spending ✅"
