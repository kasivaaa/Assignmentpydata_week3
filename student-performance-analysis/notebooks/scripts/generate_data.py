import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime

fake = Faker()
np.random.seed(42)
random.seed(42)

# ---------- CONFIG ----------
N_STUDENTS = 400
SUBJECTS = ["Mathematics", "English", "Physics", "Biology", "History", "Computer Science"]
CLASSES = ["Form 1", "Form 2", "Form 3", "Form 4"]
TERMS = ["Term 1", "Term 2", "Term 3"]
YEARS = [2023, 2024, 2025]
LOCATIONS = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]  # adjust to your context

records = []
student_pool = [(fake.name(), random.choice(["Male", "Female"]), random.randint(13, 19), random.choice(LOCATIONS))
                 for _ in range(N_STUDENTS)]

record_id = 1
for student_id, (name, gender, age, location) in enumerate(student_pool, start=1):
    student_class = random.choice(CLASSES)
    # base ability per student so their scores correlate across subjects/terms (realistic)
    base_ability = np.random.normal(65, 12)

    for year in YEARS:
        for term in TERMS:
            for subject in random.sample(SUBJECTS, k=random.randint(3, len(SUBJECTS))):
                attendance = np.clip(np.random.normal(82, 10), 40, 100)
                study_hours = np.clip(np.random.normal(3, 1.5), 0, 10)

                # performance depends on attendance + study hours + base ability + noise
                score = (
                    base_ability
                    + (attendance - 80) * 0.25
                    + study_hours * 2.5
                    + np.random.normal(0, 6)
                )
                score = float(np.clip(score, 0, 100))

                assignment_marks = np.clip(score + np.random.normal(0, 5), 0, 100)
                test_marks = np.clip(score + np.random.normal(0, 7), 0, 100)
                exam_marks = np.clip(score + np.random.normal(0, 8), 0, 100)
                final_score = round(0.2 * assignment_marks + 0.3 * test_marks + 0.5 * exam_marks, 1)

                if final_score >= 80: grade = "A"
                elif final_score >= 70: grade = "B"
                elif final_score >= 60: grade = "C"
                elif final_score >= 50: grade = "D"
                else: grade = "F"

                records.append({
                    "record_id": record_id,
                    "student_id": student_id,
                    "student_name": name,
                    "gender": gender,
                    "age": age,
                    "class": student_class,
                    "location": location,
                    "subject": subject,
                    "attendance_pct": round(attendance, 1),
                    "study_hours_per_week": round(study_hours, 1),
                    "assignment_marks": round(assignment_marks, 1),
                    "test_marks": round(test_marks, 1),
                    "exam_marks": round(exam_marks, 1),
                    "final_score": final_score,
                    "final_grade": grade,
                    "academic_term": term,
                    "academic_year": year,
                })
                record_id += 1

students_df = pd.DataFrame(records)
students_df.to_csv("data/raw/student_records.csv", index=False)
print(f"student_records.csv generated: {students_df.shape}")

# ---------- TEACHER FEEDBACK DATA ----------
TEACHERS = [fake.name() for _ in range(15)]
teacher_subject_map = {t: random.choice(SUBJECTS) for t in TEACHERS}
CATEGORIES = [
    "clarity_of_teaching", "communication", "subject_knowledge",
    "explains_concepts_well", "classroom_engagement", "availability",
    "use_of_materials", "responsiveness", "fairness_in_assessment", "overall_effectiveness"
]

feedback_records = []
fid = 1
for teacher, subject in teacher_subject_map.items():
    # teacher has a baseline quality that stays roughly consistent
    baseline = np.random.normal(3.7, 0.5)
    for year in YEARS:
        for term in TERMS:
            n_responses = random.randint(15, 40)
            for _ in range(n_responses):
                row = {"feedback_id": fid, "teacher_name": teacher, "subject": subject,
                       "academic_term": term, "academic_year": year}
                for cat in CATEGORIES:
                    rating = np.clip(np.random.normal(baseline, 0.8), 1, 5)
                    row[cat] = round(rating)
                feedback_records.append(row)
                fid += 1

feedback_df = pd.DataFrame(feedback_records)
feedback_df.to_csv("data/raw/teacher_feedback.csv", index=False)
print(f"teacher_feedback.csv generated: {feedback_df.shape}")