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
def student_progress(student_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        COUNT(*),
        AVG(score)
    FROM quiz_results
    WHERE student_id = %s
    """

    cursor.execute(query, (student_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "total_attempts": result[0],
        "average_score": result[1]
    }



# TEACHER ANALYTICS ENDPOINT

@router.get("/teacher-report")
def teacher_report():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT AVG(score) FROM quiz_results
    """

    cursor.execute(query)
    avg_score = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "average_class_score": avg_score
    }
