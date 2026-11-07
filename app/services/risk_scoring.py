from app.models import Resource


def calculate_risk_score(
    resource: Resource,
    action: str,
) -> int:

    score = 0

    # Resource Sensitivity

    if resource.sensitivity_level.value == "Public":
        score += 10

    elif resource.sensitivity_level.value == "Internal":
        score += 20

    elif resource.sensitivity_level.value == "Confidential":
        score += 50

    elif resource.sensitivity_level.value == "Restricted":
        score += 75

    elif resource.sensitivity_level.value == "Critical":
        score += 100

    # Action Risk

    action_risk = {
        "READ": 5,
        "WRITE": 15,
        "APPROVE": 25,
        "ADMIN": 40,

        "CREATE_PAYMENT": 30,
        "APPROVE_PAYMENT": 50,

        "CREATE_USER": 20,
        "APPROVE_USER": 40,
    }

    score += action_risk.get(action, 0)

    return min(score, 100)
def get_risk_level(score: int) -> str:

    if score < 30:
        return "LOW"

    if score < 70:
        return "MEDIUM"

    return "HIGH"