import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Study Plan Maker", layout="wide")
st.title("📚 Study Plan Maker")

# --- User Inputs ---
exam_date = st.date_input("📅 Exam Date")
daily_hours = st.number_input("⏰ Daily Study Hours", 2, 12, 4)
revision_cycles = st.number_input("🔁 Number of Revision Cycles", 1, 5, 2)

st.markdown("### ✏️ Enter Subject Details")

# Example starter data
if "subjects_df" not in st.session_state:
    st.session_state["subjects_df"] = pd.DataFrame({
        "Subject": ["Math", "Accounts", "Law"],
        "Weightage (%)": [40, 30, 30]
    })

edited_df = st.data_editor(
    st.session_state["subjects_df"],
    num_rows="dynamic",
    use_container_width=True
)

if st.button("Generate Study Plan"):
    today = datetime.today().date()
    days_left = (exam_date - today).days

    if days_left <= 0:
        st.error("⚠️ Exam date must be in the future!")
    else:
        subjects_df = edited_df.copy()
        subjects_df["Weightage (%)"] = subjects_df["Weightage (%)"] / subjects_df["Weightage (%)"].sum()

        plan = []
        current_day = today

        for cycle in range(1, revision_cycles + 1):
            for idx, row in subjects_df.iterrows():
                subj_days = int(days_left * row["Weightage (%)"] / revision_cycles)
                for d in range(subj_days):
                    plan.append({
                        "Date": current_day,
                        "Cycle": cycle,
                        "Subject": row["Subject"],
                        "Planned Hours": daily_hours
                    })
                    current_day += timedelta(days=1)

        df = pd.DataFrame(plan)
        st.success("✅ Study Plan Generated!")
        st.dataframe(df)

        # Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download as CSV", csv, "study_plan.csv", "text/csv")
