from fastapi import APIRouter
from app.schemas import AnswerSubmission
from app.database import get_connection
from app.queries import insert_quiz_result

router = APIRouter()

@router.post("/submit-answer")
def submit_answer(data: AnswerSubmission):

    conn = get_connection()
    cursor = conn.cursor()

    is_correct = data.student_answer == data.correct_answer
    score = 100 if is_correct else 0

    insert_quiz_result(cursor, data, is_correct, score)

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "correct": is_correct,
        "score": score
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