import pandas as pd
import streamlit as st

from grade_utils import (
    SUBJECTS,
    SUBJECT_LABELS,
    create_student_record,
    load_students,
    save_students
)


st.set_page_config(
    page_title="Add Student | Grade Management System",
    page_icon="➕",
    layout="wide"
)


def submit_student():
    student_id = st.session_state["add_student_id"].strip()
    student_name = st.session_state["add_student_name"].strip()

    if not student_id or not student_name:
        st.session_state["add_student_result"] = (
            "error",
            "Please enter both Student ID and Student Name."
        )
        return

    students = load_students()
    if students["student_id"].astype(str).str.strip().eq(student_id).any():
        st.session_state["add_student_result"] = (
            "error",
            "Student ID already exists."
        )
        return

    marks = [st.session_state[f"add_{subject}"] for subject in SUBJECTS]
    record = create_student_record(student_id, student_name, marks)
    save_students(pd.concat([students, pd.DataFrame([record])], ignore_index=True))

    st.session_state["add_student_id"] = ""
    st.session_state["add_student_name"] = ""
    for subject in SUBJECTS:
        st.session_state[f"add_{subject}"] = 0
    st.session_state["add_student_result"] = (
        "success",
        f"{student_name} added successfully."
    )


st.title("➕ Add Student")

with st.form("add_student_form"):
    st.text_input("Student ID", key="add_student_id")
    st.text_input("Student Name", key="add_student_name")

    mark_columns = st.columns(3)
    for index, subject in enumerate(SUBJECTS):
        with mark_columns[index % len(mark_columns)]:
            st.number_input(
                f"{SUBJECT_LABELS[subject]} Marks (%)",
                min_value=0,
                max_value=100,
                step=1,
                key=f"add_{subject}"
            )

    st.form_submit_button("Add Student", on_click=submit_student)

result = st.session_state.pop("add_student_result", None)
if result:
    if result[0] == "error":
        st.error(result[1])
    else:
        st.success(result[1])
