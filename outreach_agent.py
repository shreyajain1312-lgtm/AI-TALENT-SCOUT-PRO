import random

def simulate_outreach(candidate):

    interest_levels = ["high", "medium", "low"]
    interest = random.choices(
        interest_levels,
        weights=[0.4, 0.4, 0.2]
    )[0]

    responses = {
        "interest": interest,
        "notice_period": candidate["notice_period_days"],
        "salary_expectation": candidate["expected_salary"]
    }

    score_map = {"high": 90, "medium": 65, "low": 40}
    interest_score = score_map[interest]

    return responses, interest_score