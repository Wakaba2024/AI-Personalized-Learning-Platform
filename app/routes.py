from fastapi import APIRouter
from app.schemas import AnswerSubmission
from app.database import get_connection
from app.queries import insert_quiz_result
from app.ai_service import generate_quiz
from app.ai_service import simplify_explanation
from app.analytics_queries import *
from app.ai_service import generate_feedback
from app.analytics_queries import student_topic_performance
from app.ai_service import generate_learning_recommendation


router = APIRouter()

@router.post("/submit-answer")
def submit_answer(data: AnswerSubmission):

    conn = get_connection()
    cursor = conn.cursor()

    # Determine correctness
    is_correct = data.student_answer == data.correct_answer
    score = 100 if is_correct else 0

    # Generate AI feedback
    feedback = generate_feedback(
        question=data.question,
        student_answer=data.student_answer,
        correct_answer=data.correct_answer
    )

    # Save result in database
    insert_quiz_result(cursor, data, is_correct, score)

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "correct": is_correct,
        "score": score,
        "feedback": feedback
    }

# STUDENT PROGRESS ENDPOINT

@router.get("/student-progress/{student_id}")
def get_student_progress(student_id: int):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT 
        COUNT(*) AS total_quizzes,
        AVG(score) AS average_score,
        MAX(created_at) AS last_activity
    FROM quiz_results
    WHERE student_id = %s
    """

    cur.execute(query, (student_id,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "student_id": student_id,
        "total_quizzes": result[0],
        "average_score": float(result[1]) if result[1] else 0,
        "last_activity": result[2]
    }


# TEACHER ANALYTICS ENDPOINT

@router.get("/teacher-report")
def teacher_report():

    conn = get_connection()
    cur = conn.cursor()

    # Average score
    cur.execute("SELECT AVG(score) FROM quiz_results")
    avg_score = cur.fetchone()[0]

    # Students scoring below 50
    cur.execute("""
        SELECT COUNT(DISTINCT student_id)
        FROM quiz_results
        WHERE score < 50
    """)
    struggling_students = cur.fetchone()[0]

    # Most difficult topic
    cur.execute("""
        SELECT t.topic_name, AVG(q.score) AS avg_score
        FROM quiz_results q
        JOIN topics t ON q.topic_id = t.topic_id
        GROUP BY t.topic_name
        ORDER BY avg_score ASC
        LIMIT 1
    """)

    difficult_topic = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "average_score": float(avg_score) if avg_score else 0,
        "students_below_50": struggling_students,
        "most_difficult_topic": difficult_topic[0] if difficult_topic else None
    }


# Adaptive Difficulty Logic here we determine difficulty based on student performance.

def determine_difficulty(student_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT AVG(score), AVG(time_spent_seconds)
        FROM quiz_results
        WHERE student_id = %s
    """, (student_id,))

    avg_score, avg_time = cur.fetchone()

    cur.close()
    conn.close()

    if avg_score is None:
        return "easy"

    if avg_score >= 80 and avg_time < 20:
        return "hard"

    elif avg_score >= 50:
        return "medium"

    else:
        return "easy"
    
    # Quiz Generation Endpoint

@router.get("/generate-quiz/{topic}")
def generate_quiz_question(topic: str):

    quiz = generate_quiz(topic, "medium")

    return {
        "topic": topic,
        "quiz": quiz
    }


# Adaptive Quiz Endpoint (This makes learning personalized)

@router.get("/adaptive-quiz/{student_id}/{topic}")
def adaptive_quiz(student_id: int, topic: str):

    difficulty = determine_difficulty(student_id)

    quiz = generate_quiz(topic, difficulty)

    return {
        "student_id": student_id,
        "difficulty": difficulty,
        "quiz": quiz
    }


# Simplified Explanation Endpoint

@router.get("/simple-explanation/{topic}")
def simple_explanation(topic: str):

    explanation = simplify_explanation(topic)

    return {
        "topic": topic,
        "explanation": explanation
    }

# Student Performance Endpoint
@router.get("/analytics/student-performance")
def student_performance():

    conn = get_connection()
    cur = conn.cursor()

    data = average_score_per_student(cur)

    cur.close()
    conn.close()

    return {"student_performance": data}

# Topic Performance Endpoint

@router.get("/analytics/topic-performance")
def topic_performance():

    conn = get_connection()
    cur = conn.cursor()

    data = average_score_per_topic(cur)

    cur.close()
    conn.close()

    return {"topic_performance": data}

# Performance Trend Endpoint

@router.get("/analytics/performance-trend")
def performance_trend_report():

    conn = get_connection()
    cur = conn.cursor()

    data = performance_trend(cur)

    cur.close()
    conn.close()

    return {"trend": data}

# Struggling Students Endpoint

@router.get("/analytics/struggling-students")
def struggling():

    conn = get_connection()
    cur = conn.cursor()

    data = struggling_students(cur)

    cur.close()
    conn.close()

    return {"students_below_50": data}

# At-Risk Students Endpoint

@router.get("/analytics/at-risk-students")
def at_risk():

    conn = get_connection()
    cur = conn.cursor()

    data = at_risk_students(cur)

    cur.close()
    conn.close()

    return {"at_risk_students": data}

# Time Spent Analytics Endpoint

@router.get("/analytics/time-per-topic")
def time_per_topic():

    conn = get_connection()
    cur = conn.cursor()

    data = average_time_per_topic(cur)

    cur.close()
    conn.close()

    return {"time_per_topic": data}


# Recommendation Endpoint

@router.get("/learning-recommendations/{student_id}")
def learning_recommendations(student_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    performance = student_topic_performance(cursor, student_id)

    recommendations = []

    for topic, avg_score in performance:

        advice = generate_learning_recommendation(topic, avg_score)

        recommendations.append({
            "topic": topic,
            "average_score": avg_score,
            "recommendation": advice
        })

    cursor.close()
    conn.close()

    return {
        "student_id": student_id,
        "recommendations": recommendations
    }