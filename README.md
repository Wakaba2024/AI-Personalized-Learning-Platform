# AI-Powered Personalized Learning Platform

An **AI-driven adaptive learning platform** that personalizes quizzes,
analyzes student performance, and provides teacher insights using
**FastAPI, PostgreSQL, SQL analytics, Mistral AI, and Streamlit
dashboards**.

------------------------------------------------------------------------

# Project Overview

This project demonstrates how **AI engineering, backend development, and
data analytics** can be combined to create an intelligent educational
system.

The platform:

-   Generates **AI-powered quizzes**
-   Provides **real-time feedback**
-   Tracks **student performance**
-   Detects **struggling students**
-   Identifies **difficult topics**
-   Visualizes insights in a **teacher dashboard**

The goal is to simulate a **modern AI-powered EdTech platform** that
supports personalized education and data-driven decision making.

------------------------------------------------------------------------

# Key Features

## 1. AI-Powered Quiz Generation

The platform integrates **Mistral AI** to dynamically generate quiz
questions based on topics.

Capabilities: - Topic-based quiz generation - Adaptive difficulty
questions - AI-generated explanations - Simplified explanations for
accessibility

Example endpoint:

    GET /generate-quiz/{topic}

Example response:

    {
     "question": "What is 5 + 7?",
     "options": ["10", "11", "12", "13"],
     "correct_answer": "12",
     "explanation": "5 plus 7 equals 12."
    }

------------------------------------------------------------------------

# 2. Real-Time AI Feedback

When a student submits an answer:

1.  The system evaluates correctness
2.  AI generates feedback
3.  Results are stored in PostgreSQL
4.  Student progress updates instantly

Endpoint:

    POST /submit-answer

Example response:

    {
     "correct": false,
     "score": 0,
     "feedback": "The correct answer is 12 because 5 + 7 equals 12."
    }

------------------------------------------------------------------------

# 3. Adaptive Learning

The platform adjusts quiz difficulty based on student performance.

Endpoint:

    GET /adaptive-quiz/{student_id}/{topic}

------------------------------------------------------------------------

# 4. Student Data Collection

The system stores student interaction data including:

-   Student answers
-   Quiz scores
-   Correctness
-   Time spent on questions
-   Topic performance

------------------------------------------------------------------------

# 5. SQL Analytics Engine

Student data is analyzed using SQL queries.

Metrics calculated:

- Average Score Per Student

- Average Score Per Topic

- Struggling Students

------------------------------------------------------------------------

# 6. Teacher Analytics API

Teachers can retrieve insights through analytics endpoints.

Examples:

    GET /analytics/student-performance
    GET /analytics/topic-performance
    GET /analytics/performance-trend
    GET /analytics/struggling-students
    GET /analytics/at-risk-students

These endpoints allow teachers to:

-   Identify struggling students
-   Detect difficult topics
-   Monitor learning trends

------------------------------------------------------------------------

# 7. Streamlit Teacher Dashboard

A **Streamlit dashboard** visualizes learning analytics.

Teachers can view:

-   Student performance tables
-   Topic difficulty metrics
-   Performance trends
-   At-risk students

Run the dashboard:

    streamlit run dashboard.py

------------------------------------------------------------------------

# System Architecture

    Students
       ↓
    FastAPI Backend
       ↓
    PostgreSQL Database
       ↓
    AI Engine (Mistral)
       ↓
    SQL Analytics
       ↓
    Streamlit Teacher Dashboard

------------------------------------------------------------------------

# Technology Stack

Backend: - FastAPI - Python

Database: - PostgreSQL - psycopg2

AI: - Mistral AI API

Data Analytics: - SQL

Visualization: - Streamlit

Environment Management: - UV

------------------------------------------------------------------------

# Project Structure

    AI_Learning_Platform
    │
    ├── app
    │   ├── main.py
    │   ├── routes.py
    │   ├── database.py
    │   ├── schemas.py
    │   ├── ai_service.py
    │   └── settings.py
    │
    ├── dashboard.py
    ├── README.md
    └── requirements.txt

------------------------------------------------------------------------

# Running the Project

## 1 Install Dependencies

    uv sync

## 2 Start Backend

    uvicorn app.main:app --reload

API docs:

    http://127.0.0.1:8000/docs

## 3 Run Dashboard

    streamlit run dashboard.py

------------------------------------------------------------------------

# Example Workflow

Student submits answer

    POST /submit-answer

System processes:

1.  Evaluate answer
2.  Generate AI explanation
3.  Store results
4.  Update performance metrics

Teacher views analytics

    GET /analytics/student-performance

Dashboard visualizes results.






