import streamlit as st
import pandas as pd
from datetime import datetime
from planner import generate_study_plan
from pdf_exporter import export_plan_to_pdf

st.set_page_config(page_title="Study Plan Maker", layout="wide")
st.title("📚 Study Plan Maker")

# --- User Inputs ---
exam_date = st.date_input("📅 Exam Date")
daily_hours = st.number_input("⏰ Daily Study Hours", 2, 12, 6)
revision_cycles = st.number_input("🔁 Number of Revision Cycles", 1, 5, 2)

st.markdown("### ✏️ Enter Subject Details")

if "subjects_df" not in st.session_state:
    st.session_state["subjects_df"] = pd.DataFrame({
        "Subject": ["Math", "Accounts", "Law"],
        "Hours Needed": [60, 40, 30],
    })

edited_df = st.data_editor(
    st.session_state["subjects_df"],
    num_rows="dynamic",
    use_container_width=True
)

if st.button("Generate Study Plan"):
    df, msg = generate_study_plan(exam_date, edited_df, daily_hours, revision_cycles)

    if df is None:
        st.error(msg)
    else:
        st.success(msg)
        st.dataframe(df)

        grouped = df.groupby("Date").apply(
            lambda x: ", ".join(f"{r['Subject']} ({r['Planned Hours']}h)" for _, r in x.iterrows())
        ).reset_index(name="Daily Plan")

        st.markdown("### 📅 Daily Schedule")
        st.dataframe(grouped)

        # Download CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "study_plan.csv", "text/csv")

        # Generate and Download PDF
        pdf_file = "study_plan.pdf"
        export_plan_to_pdf(df, pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name=pdf_file, mime="application/pdf")
