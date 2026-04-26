import streamlit as st
import pandas as pd
from jd_parser import parse_jd_llm
from candidate_data import generate_candidates
from matching_engine import calculate_match
from outreach_agent import simulate_outreach
from scoring import final_score
from explainability import explain
from resume_parser import parse_resume

st.set_page_config(page_title="AI Talent Scout PRO", layout="wide")

# 🎨 STYLE
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# 🚀 HEADER
st.title("🚀 AI Talent Scout PRO")
st.caption("End-to-end AI hiring intelligence system")

# 📂 SIDEBAR FILTERS
st.sidebar.header("🔎 Filters")

min_exp = st.sidebar.slider("Min Experience", 0, 10, 2)
location_filter = st.sidebar.selectbox("Location", ["All", "Remote", "Bangalore", "Hyderabad"])
available_only = st.sidebar.checkbox("Only Available Candidates")

search_name = st.sidebar.text_input("Search Candidate")

# 📄 JD INPUT
jd_text = st.text_area("Paste Job Description")

# 📎 RESUME UPLOAD
uploaded_file = st.file_uploader("Upload Resume (txt only)", type=["txt"])

resume_data = None
if uploaded_file:
    resume_data = parse_resume(uploaded_file)
    st.success(f"Parsed Resume: {resume_data}")

if st.button("Find Candidates"):

    jd = parse_jd_llm(jd_text)
    candidates = generate_candidates()

    results = []

    for c in candidates:

        # APPLY FILTERS
        if c["years_of_experience"] < min_exp:
            continue

        if location_filter != "All" and c["location"] != location_filter:
            continue

        if available_only and not c["availability"]:
            continue

        if search_name and search_name.lower() not in c["name"].lower():
            continue

        match = calculate_match(0.7, c, jd)
        convo, interest = simulate_outreach(c)
        final = final_score(match, interest)

        results.append((c, match, interest, final, convo))

    # SORT OPTION
    sort_by = st.selectbox("Sort By", ["Final Score", "Match Score"])

    if sort_by == "Final Score":
        results = sorted(results, key=lambda x: x[3], reverse=True)
    else:
        results = sorted(results, key=lambda x: x[1], reverse=True)

    top = results[:10]

    st.subheader("🏆 Top Candidates")

    chart_data = []

    for c, m, i, f, convo in top:

        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(f"### 👤 {c['name']}")
            st.caption(f"{c['current_role']} • {c['location']} • {c['years_of_experience']} yrs")

            col1, col2, col3 = st.columns(3)
            col1.metric("Match", m)
            col1.progress(int(m))

            col2.metric("Interest", i)
            col2.progress(int(i))

            col3.metric("Final", f)
            col3.progress(int(f))

            st.markdown("**Skills Match:**")
            exp = explain(c, jd)
            st.write(exp)

            st.markdown("**Insights:**")
            st.json(convo)

            # ACTIONS
            colA, colB, colC = st.columns(3)
            colA.button(f"Invite {c['name']}", key=f"i_{c['name']}")
            colB.button(f"Hold {c['name']}", key=f"h_{c['name']}")
            colC.button(f"Reject {c['name']}", key=f"r_{c['name']}")

            st.markdown('</div>', unsafe_allow_html=True)

            chart_data.append({
                "Name": c["name"],
                "Final Score": f,
                "Match Score": m
            })

    # 📊 CHART
    st.subheader("📊 Score Comparison")
    df = pd.DataFrame(chart_data)
    st.bar_chart(df.set_index("Name"))

    # 📥 EXPORT
    st.subheader("📥 Export Shortlist")
    st.download_button("Download CSV", df.to_csv(), "shortlist.csv")