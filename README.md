# Grade Management System

A multipage student grade management application built with Streamlit. It stores student records in a CSV file and provides student entry, record search and editing, performance reports, charts, and Excel export.

## Features

- Add students with a unique student ID and marks for five subjects.
- Assign a subject grade for each mark. Marks below 35 receive an `F`.
- Calculate each student's total, average percentage, and CGPA.
- Search and sort student records; edit names and marks with calculated fields refreshed on save.
- View class statistics, the top five students, and grade distribution charts.
- Download student records as an Excel workbook.

## Project Structure

```text
grade-management-system/
|-- app.py
|-- grade_utils.py
|-- requirements.txt
|-- README.md
|-- data/
|   `-- students.csv
`-- pages/
    |-- 1_Add_Student.py
    |-- 2_Student_Records.py
    `-- 3_Reports.py
```

The `data/students.csv` file is created when a record is first saved if it does not already exist.

## Requirements

- Python 3.10 or later
- Packages listed in `requirements.txt`

## Installation and Run

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints the local URL after the server starts, usually <http://localhost:8501>.

## Pages

- **Home:** Class overview and navigation to the application pages.
- **Add Student:** Enter a student ID, name, and subject marks. Duplicate IDs are rejected. The input fields clear after a successful save.
- **Student Records:** Search and sort the records table. Student names and subject marks are editable; IDs and calculated values are read-only. Saving edits recalculates subject grades, totals, average, and CGPA.
- **Reports:** Review pass/fail and class statistics, the top five students and charts, and download an Excel report.

## Grade Calculations

The average percentage is the arithmetic mean of the five subject marks. Subject grades use these bands:

| Mark | Grade |
| --- | --- |
| Below 35 | F |
| 35-59 | D |
| 60-69 | C |
| 70-79 | B |
| 80-89 | A |
| 90-100 | A+ |

CGPA is calculated as `average percentage / 9.5`, rounded to two decimal places and capped at 10. A student is counted as failed if at least one subject mark is below 35.

## Dependencies

Dependencies are declared in `requirements.txt`: Streamlit, pandas, Matplotlib, and openpyxl. The Excel download uses openpyxl to generate the `.xlsx` workbook.
