import pandas as pd
import streamlit as st

from grade_utils import (
    SUBJECTS,
    SUBJECT_LABELS,
    load_students,
    recalculate_student_data,
    save_students
)


st.set_page_config(
    page_title="Student Records | Grade Management System",
    page_icon="📋",
    layout="wide"
)


def subject_column_config():
    config = {
        "student_id": st.column_config.TextColumn("Student ID"),
        "student_name": st.column_config.TextColumn(
            "Student Name",
            required=True
        ),
        "_row_index": None
    }
    for subject in SUBJECTS:
        config[subject] = st.column_config.NumberColumn(
            f"{SUBJECT_LABELS[subject]} Marks",
            min_value=0,
            max_value=100,
            step=1
        )
        config[f"{subject}_grade"] = st.column_config.TextColumn(
            f"{SUBJECT_LABELS[subject]} Grade"
        )
    config.update({
        "total": st.column_config.NumberColumn("Total"),
        "average": st.column_config.NumberColumn("Average (%)", format="%.2f"),
        "cgpa": st.column_config.NumberColumn("CGPA", format="%.2f")
    })
    return config


if st.session_state.pop("records_saved", False):
    st.success("Student records updated.")

st.title("📋 Student Records")
students = load_students()

if students.empty:
    st.info("No students added yet.")
else:
    search_col, sort_col, order_col = st.columns([2, 1, 1])
    with search_col:
        search = st.text_input(
            "Search by name or ID",
            placeholder="Enter a student name or ID"
        ).strip().lower()
    with sort_col:
        sort_by = st.selectbox(
            "Sort By",
            ["student_name", "student_id", "total", "average", "cgpa"]
        )
    with order_col:
        ascending = st.selectbox("Order", ["Descending", "Ascending"]) == "Ascending"

    filtered = students
    if search:
        matches = (
            students["student_name"].astype(str).str.lower().str.contains(search)
            | students["student_id"].astype(str).str.lower().str.contains(search)
        )
        filtered = students[matches]
    filtered = filtered.sort_values(sort_by, ascending=ascending)

    st.caption(f"Showing {len(filtered)} of {len(students)} students")
    editor_data = filtered.copy()
    editor_data["_row_index"] = editor_data.index
    disabled_columns = [
        "_row_index",
        "student_id",
        "total",
        "average",
        "cgpa",
        *(f"{subject}_grade" for subject in SUBJECTS)
    ]

    with st.form("edit_student_records"):
        edited = st.data_editor(
            editor_data,
            hide_index=True,
            use_container_width=True,
            num_rows="fixed",
            disabled=disabled_columns,
            column_config=subject_column_config(),
            key="student_records_editor"
        )
        save_changes = st.form_submit_button("Save Changes")

    if save_changes:
        names = edited["student_name"].fillna("").astype(str).str.strip()
        marks = edited[list(SUBJECTS)].apply(pd.to_numeric, errors="coerce")
        if names.eq("").any():
            st.error("Student names cannot be empty.")
        elif marks.isna().any().any() or marks.lt(0).any().any() or marks.gt(100).any().any():
            st.error("Subject marks must be numbers between 0 and 100.")
        else:
            editable = edited.copy()
            editable["student_name"] = names
            editable.loc[:, list(SUBJECTS)] = marks
            row_indexes = editable["_row_index"].astype(int)
            students.loc[row_indexes, ["student_name", *SUBJECTS]] = editable[
                ["student_name", *SUBJECTS]
            ].to_numpy()
            save_students(recalculate_student_data(students))
            st.session_state["records_saved"] = True
            st.rerun()
