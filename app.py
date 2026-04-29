import streamlit as st
import mysql.connector
import pandas as pd

# DB Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tanishL@123",
        database="student_management"
    )

st.title("🎓 Student Attendance & Grade Management System")

menu = st.sidebar.selectbox("Menu", [
    "Add Student",
    "Add Attendance",
    "Add Grade",
    "View Report",
    "Attendance %"
])

# ------------------ ADD STUDENT ------------------
if menu == "Add Student":
    st.subheader("Add Student")

    sid = st.number_input("Student ID")
    name = st.text_input("Name")
    email = st.text_input("Email")
    dept = st.text_input("Department")

    if st.button("Add"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Students VALUES (%s,%s,%s,%s)",
            (sid, name, email, dept)
        )
        conn.commit()
        st.success("Student added!")

# ------------------ ADD ATTENDANCE ------------------
elif menu == "Add Attendance":
    st.subheader("Mark Attendance")

    sid = st.number_input("Student ID")
    cid = st.number_input("Course ID")
    date = st.date_input("Date")
    status = st.selectbox("Status", ["Present", "Absent"])

    if st.button("Submit"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Attendance (student_id, course_id, date, status) VALUES (%s,%s,%s,%s)",
            (sid, cid, date, status)
        )
        conn.commit()
        st.success("Attendance added!")

# ------------------ ADD GRADE ------------------
elif menu == "Add Grade":
    st.subheader("Add Grade")

    sid = st.number_input("Student ID")
    cid = st.number_input("Course ID")
    marks = st.number_input("Marks")

    if st.button("Calculate & Save"):
        if marks >= 90:
            grade = 'A'
        elif marks >= 75:
            grade = 'B'
        elif marks >= 60:
            grade = 'C'
        else:
            grade = 'D'

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Grades (student_id, course_id, marks, grade) VALUES (%s,%s,%s,%s)",
            (sid, cid, marks, grade)
        )
        conn.commit()
        st.success(f"Grade {grade} added!")

# ------------------ VIEW REPORT ------------------
elif menu == "View Report":
    st.subheader("Student Report")

    conn = get_connection()
    query = """
    SELECT s.name, c.course_name, g.marks, g.grade
    FROM Students s
    JOIN Grades g ON s.student_id = g.student_id
    JOIN Courses c ON g.course_id = c.course_id
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

# ------------------ ATTENDANCE % ------------------
elif menu == "Attendance %":
    st.subheader("Attendance Percentage")

    conn = get_connection()
    query = """
    SELECT student_id, course_id,
    COUNT(CASE WHEN status='Present' THEN 1 END)*100.0/COUNT(*) AS percentage
    FROM Attendance
    GROUP BY student_id, course_id
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)