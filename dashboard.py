import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.title("📊 AI Learning Platform - Teacher Dashboard")

st.sidebar.header("Analytics Options")

option = st.sidebar.selectbox(
    "Select Report",
    [
        "Student Performance",
        "Topic Performance",
        "Performance Trend",
        "Struggling Students",
        "At Risk Students"
    ]
)

# STUDENT PERFORMANCE
if option == "Student Performance":

    st.header("Student Performance")

    data = requests.get(f"{API_URL}/analytics/student-performance").json()

    df = pd.DataFrame(
        data["student_performance"],
        columns=["Student ID", "Average Score", "Quizzes Taken"]
    )

    st.dataframe(df)


# TOPIC PERFORMANCE
elif option == "Topic Performance":

    st.header("Topic Performance")

    data = requests.get(f"{API_URL}/analytics/topic-performance").json()

    df = pd.DataFrame(
        data["topic_performance"],
        columns=["Topic", "Average Score", "Attempts"]
    )

    st.dataframe(df)


# PERFORMANCE TREND
elif option == "Performance Trend":

    st.header("Performance Trend Over Time")

    data = requests.get(f"{API_URL}/analytics/performance-trend").json()

    df = pd.DataFrame(
        data["trend"],
        columns=["Date", "Average Score", "Quizzes Taken"]
    )

    st.line_chart(df.set_index("Date")["Average Score"])


# STRUGGLING STUDENTS
elif option == "Struggling Students":

    st.header("Students Below 50%")

    data = requests.get(f"{API_URL}/analytics/struggling-students").json()

    df = pd.DataFrame(
        data["students_below_50"],
        columns=["Student ID", "Average Score", "Quizzes Taken"]
    )

    st.dataframe(df)


# AT RISK STUDENTS
elif option == "At Risk Students":

    st.header("At Risk Students")

    data = requests.get(f"{API_URL}/analytics/at-risk-students").json()

    df = pd.DataFrame(
        data["at_risk_students"],
        columns=["Student ID", "Quizzes Taken", "Average Score"]
    )

    st.dataframe(df)