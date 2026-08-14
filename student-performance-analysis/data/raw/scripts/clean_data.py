import pandas as pd

# ---------- LOAD ----------
students = pd.read_csv("data/raw/student_records.csv")
feedback = pd.read_csv("data/raw/teacher_feedback.csv")

# ---------- MISSING VALUES ----------
print("Missing values (students):\n", students.isnull().sum())
print("Missing values (feedback):\n", feedback.isnull().sum())

# Example handling: fill numeric gaps with column median, drop rows missing an ID
num_cols = ["attendance_pct", "study_hours_per_week", "assignment_marks",
            "test_marks", "exam_marks", "final_score"]
students[num_cols] = students[num_cols].fillna(students[num_cols].median())
students = students.dropna(subset=["student_id"])

# ---------- DUPLICATES ----------
students = students.drop_duplicates()
feedback = feedback.drop_duplicates()

# ---------- DATA TYPES ----------
students["academic_year"] = students["academic_year"].astype(int)
students["gender"] = students["gender"].astype("category")
students["final_grade"] = students["final_grade"].astype("category")

# ---------- CONSISTENCY CHECKS ----------
# Clip any impossible values (e.g., attendance > 100 or negative)
students["attendance_pct"] = students["attendance_pct"].clip(0, 100)
students["study_hours_per_week"] = students["study_hours_per_week"].clip(0, None)

# Standardize text fields
students["subject"] = students["subject"].str.strip().str.title()
students["student_name"] = students["student_name"].str.strip()

# ---------- RENAME FOR CLARITY (example) ----------
students = students.rename(columns={"attendance_pct": "attendance_percent"})

# ---------- ORDER TERMS PROPERLY (for time-series later) ----------
term_order = {"Term 1": 1, "Term 2": 2, "Term 3": 3}
students["term_number"] = students["academic_term"].map(term_order)
students["period"] = students["academic_year"].astype(str) + "-" + students["academic_term"]

# ---------- SAVE CLEANED DATA ----------
students.to_csv("data/cleaned/student_records_clean.csv", index=False)
feedback.to_csv("data/cleaned/teacher_feedback_clean.csv", index=False)

print("Cleaned files saved to data/cleaned/")