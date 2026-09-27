from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from openpyxl.utils import get_column_letter

from grade_utils import SUBJECTS, SUBJECT_LABELS, load_students


st.set_page_config(
    page_title="Reports | Grade Management System",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Reports")
students = load_students()

if students.empty:
    st.info("Add students to view class reports.")
else:
    total_students = len(students)
    class_average = students["average"].mean()
    failed_students = int(students[list(SUBJECTS)].lt(35).any(axis=1).sum())
    passed_students = total_students - failed_students

    metric_columns = st.columns(4)
    metric_columns[0].metric("Students", total_students)
    metric_columns[1].metric("Class Average", f"{class_average:.2f}%")
    metric_columns[2].metric("Passed", passed_students)
    metric_columns[3].metric("Failed", failed_students)

    st.subheader("🏆 Top 5 Students")
    toppers = students.sort_values("average", ascending=False).head(5)
    st.dataframe(
        toppers[["student_id", "student_name", "total", "average", "cgpa"]],
        use_container_width=True,
        hide_index=True
    )

    top_chart, subject_chart = st.columns(2)
    with top_chart:
        figure, axis = plt.subplots(figsize=(8, 4))
        bars = axis.barh(toppers["student_name"], toppers["average"])
        axis.invert_yaxis()
        axis.set_xlim(0, 110)
        axis.set_xlabel("Average Percentage")
        axis.set_title("Top 5 Students by Average")
        axis.bar_label(bars, fmt="%.2f%%", padding=4)
        st.pyplot(figure)
        plt.close(figure)

    with subject_chart:
        grade_counts = pd.DataFrame({
            SUBJECT_LABELS[subject]: students[f"{subject}_grade"].value_counts()
            for subject in SUBJECTS
        }).reindex(["F", "D", "C", "B", "A", "A+"], fill_value=0)
        figure, axis = plt.subplots(figsize=(8, 4))
        grade_counts.plot(kind="bar", ax=axis)
        axis.set_xlabel("Subject Grade")
        axis.set_ylabel("Number of Students")
        axis.set_title("Subject Grade Distribution")
        axis.legend(title="Subject")
        st.pyplot(figure)
        plt.close(figure)

    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        students.to_excel(writer, index=False, sheet_name="Students")
        worksheet = writer.sheets["Students"]
        minimum_widths = {"student_id": 18, "student_name": 28}
        for index, column in enumerate(students.columns, start=1):
            values_width = students[column].fillna("").astype(str).str.len().max()
            content_width = max(len(column), int(values_width or 0))
            width = max(content_width + 2, minimum_widths.get(column, 12))
            worksheet.column_dimensions[get_column_letter(index)].width = min(width, 50)

    st.download_button(
        "Download Excel Report",
        data=excel_file.getvalue(),
        file_name="student_grade_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
