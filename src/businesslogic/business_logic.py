# Risk Classification

def get_risk_level(prob):
    if prob < 0.30:
        return "LOW"
    elif prob < 0.65:
        return "MEDIUM"
    else:
        return "HIGH"


# Retention Actions Mapping

def get_retention_action(risk_level):
    actions = {
        "LOW": "Send engagement email",
        "MEDIUM": "Offer discount coupon",
        "HIGH": "Call customer + Premium retention offer"
    }
    return actions[risk_level]
