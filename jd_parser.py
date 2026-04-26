import re

SKILLS_DB = [
    "react", "typescript", "javascript", "node", "aws",
    "docker", "html", "css", "angular", "vue"
]

def parse_jd_llm(jd_text):
    jd_text_lower = jd_text.lower()

    skills = [s.capitalize() for s in SKILLS_DB if s in jd_text_lower]

    exp_match = re.search(r'(\d+)\+?\s*years', jd_text_lower)
    experience = int(exp_match.group(1)) if exp_match else 2

    role = "Frontend Engineer" if "frontend" in jd_text_lower else "Software Engineer"

    location = "Remote" if "remote" in jd_text_lower else "Onsite"

    return {
        "role": role,
        "skills": skills,
        "experience": experience,
        "location": location
    }