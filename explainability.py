def explain(candidate, jd):
    exp = []

    for skill in jd["skills"]:
        if skill in candidate["skills"]:
            exp.append(f"✅ {skill}")
        else:
            exp.append(f"❌ {skill}")

    return exp