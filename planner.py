import pandas as pd
from datetime import datetime, timedelta

def generate_study_plan(exam_date, subjects_df, daily_hours, revision_cycles):
    today = datetime.today().date()
    days_left = (exam_date - today).days

    if days_left <= 0:
        return None, "⚠️ Exam date must be in the future!"

    subjects_df = subjects_df.copy()
    subjects_df["Weightage (%)"] = subjects_df["Weightage (%)"] / subjects_df["Weightage (%)"].sum()

    plan = []
    current_day = today

    for cycle in range(1, revision_cycles + 1):
        for _, row in subjects_df.iterrows():
            subj_days = int(days_left * row["Weightage (%)"] / revision_cycles)
            for _ in range(subj_days):
                plan.append({
                    "Date": current_day,
                    "Cycle": cycle,
                    "Subject": row["Subject"],
                    "Planned Hours": daily_hours
                })
                current_day += timedelta(days=1)

    df = pd.DataFrame(plan)
    return df, "✅ Study Plan Generated!"
