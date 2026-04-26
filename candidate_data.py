import random

def generate_candidates():
    skills_pool = ["React", "Vue", "Angular", "Node.js", "AWS", "Docker", "JavaScript", "TypeScript"]

    candidates = []
    for i in range(25):
        candidates.append({
            "name": f"Candidate {i+1}",
            "skills": random.sample(skills_pool, k=4),
            "years_of_experience": random.randint(1, 10),
            "current_role": "Frontend Engineer",
            "location": random.choice(["Remote", "Bangalore", "Hyderabad"]),
            "availability": random.choice([True, False]),
            "expected_salary": random.randint(8, 30),
            "notice_period_days": random.choice([15, 30, 60])
        })
    return candidates