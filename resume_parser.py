import streamlit as st

def parse_resume(uploaded_file):
    text = uploaded_file.read().decode("utf-8", errors="ignore")

    skills = []
    keywords = ["react", "python", "aws", "docker", "sql"]

    for k in keywords:
        if k in text.lower():
            skills.append(k.capitalize())

    return {
        "name": uploaded_file.name,
        "skills": skills,
        "experience": 3
    }