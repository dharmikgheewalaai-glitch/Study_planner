import pandas as pd
from datetime import datetime, timedelta

def generate_study_plan(exam_date, subjects_df, daily_hours, revision_cycles):
    today = datetime.today().date()
    days_left = (exam_date - today).days

    if days_left <= 0:
        return None, "⚠️ Exam date must be in the future!"

    subjects_df = subjects_df.copy()

    # Normalize weightage based on "Hours Needed" if available
    if "Hours Needed" in subjects_df.columns and subjects_df["Hours Needed"].sum() > 0:
        subjects_df["Weight"] = subjects_df["Hours Needed"] / subjects_df["Hours Needed"].sum()
    elif "Weightage (%)" in subjects_df.columns:
        subjects_df["Weight"] = subjects_df["Weightage (%)"] / subjects_df["Weightage (%)"].sum()
    else:
        return None, "⚠️ Please provide Hours Needed or Weightage %"

    plan = []
    current_day = today

    for cycle in range(1, revision_cycles + 1):
        for d in range(days_left // revision_cycles):
            daily_plan = []
            for _, row in subjects_df.iterrows():
                subj_hours = round(daily_hours * row["Weight"], 2)
                daily_plan.append({
                    "Date": current_day,
                    "Cycle": cycle,
                    "Subject": row["Subject"],
                    "Planned Hours": subj_hours
                })
            plan.extend(daily_plan)
            current_day += timedelta(days=1)

    df = pd.DataFrame(plan)
    return df, "✅ Study Plan Generated!"
