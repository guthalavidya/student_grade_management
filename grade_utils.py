import csv
from pathlib import Path

import pandas as pd


SUBJECTS = ("python", "dmgt", "java", "ads", "ids")
SUBJECT_LABELS = {
    "python": "Python",
    "dmgt": "DMGT",
    "java": "Java",
    "ads": "ADS",
    "ids": "IDS"
}
DATA_FILE = Path(__file__).resolve().parent / "data" / "students.csv"
LEGACY_COLUMNS = [
    "student_id",
    "student_name",
    "python",
    "dmgt",
    "java",
    "ads",
    "ids",
    "total",
    "average",
    "grade"
]
STUDENT_COLUMNS = [
    "student_id",
    "student_name",
    "python",
    "python_grade",
    "dmgt",
    "dmgt_grade",
    "java",
    "java_grade",
    "ads",
    "ads_grade",
    "ids",
    "ids_grade",
    "total",
    "average",
    "cgpa"
]


def calculate_total(marks):
    return sum(marks)


def calculate_average(marks):
    return sum(marks) / len(marks)


def calculate_cgpa(average):
    return round(min(average / 9.5, 10), 2)


def calculate_subject_grade(mark):
    if mark < 35:
        return "F"
    elif mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    else:
        return "D"


def recalculate_student_data(df):
    df = df.copy()
    for subject in SUBJECTS:
        df[subject] = pd.to_numeric(df[subject])
        df[f"{subject}_grade"] = df[subject].apply(calculate_subject_grade)

    marks = df[list(SUBJECTS)]
    df["total"] = marks.sum(axis=1)
    df["average"] = marks.mean(axis=1).round(2)
    df["cgpa"] = df["average"].apply(calculate_cgpa)
    df = df.drop(columns=["grade"], errors="ignore")
    return df[[column for column in STUDENT_COLUMNS if column in df.columns]]


def load_students():
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=STUDENT_COLUMNS)

    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader, [])
        rows = list(reader)

    if rows and len(headers) != len(LEGACY_COLUMNS) and all(
        len(row) == len(LEGACY_COLUMNS) for row in rows
    ):
        df = pd.DataFrame(rows, columns=LEGACY_COLUMNS)
    else:
        df = pd.read_csv(DATA_FILE)

    for subject in SUBJECTS:
        if subject not in df.columns:
            df[subject] = 0

    return recalculate_student_data(df)


def save_students(df):
    DATA_FILE.parent.mkdir(exist_ok=True)
    ordered = df[[column for column in STUDENT_COLUMNS if column in df.columns]]
    ordered.to_csv(DATA_FILE, index=False)


def create_student_record(student_id, student_name, marks):
    record = {
        "student_id": str(student_id).strip(),
        "student_name": str(student_name).strip()
    }
    record.update(dict(zip(SUBJECTS, marks)))
    return recalculate_student_data(pd.DataFrame([record])).iloc[0].to_dict()