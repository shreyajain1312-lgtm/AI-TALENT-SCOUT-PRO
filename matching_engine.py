from sklearn.metrics.pairwise import cosine_similarity

def similarity_score(jd_emb, cand_emb):
    return cosine_similarity([jd_emb], [cand_emb])[0][0]

def calculate_match(similarity, candidate, jd):
    # normalize similarity (0–1)
    sim = similarity / 100  

    score = sim * 70  # max 70

    # Experience
    if candidate["years_of_experience"] >= jd.get("experience", 2):
        score += 20
    else:
        score += 10

    # Availability
    if candidate["availability"]:
        score += 10

    return round(min(score, 100), 2)  # cap at 100