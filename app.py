import streamlit as st

from grade_utils import load_students


st.set_page_config(
    page_title="Grade Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Grade Management System")
st.write("Manage student marks, academic records, and performance reports.")

students = load_students()
if students.empty:
    st.info("No student records yet. Add a student to get started.")
else:
    subjects = ("python", "dmgt", "java", "ads", "ids")
    failed_count = int(students[list(subjects)].lt(35).any(axis=1).sum())
    total_count = len(students)
    average = students["average"].mean()

    total_col, average_col, passed_col, failed_col = st.columns(4)
    total_col.metric("Students", total_count)
    average_col.metric("Class Average", f"{average:.2f}%")
    passed_col.metric("Passed", total_count - failed_count)
    failed_col.metric("Failed", failed_count)

st.divider()
add_col, records_col, reports_col = st.columns(3)
with add_col:
    st.page_link(
        "pages/1_Add_Student.py",
        label="Add Student",
        icon="➕"
    )
with records_col:
    st.page_link(
        "pages/2_Student_Records.py",
        label="Student Records",
        icon="📋"
    )
with reports_col:
    st.page_link(
        "pages/3_Reports.py",
        label="Reports",
        icon="📊"
    )
