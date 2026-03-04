def insert_quiz_result(cursor, data, is_correct, score):

    query = """
    INSERT INTO quiz_results
    (student_id, topic_id, question, student_answer, correct_answer,
    is_correct, score, time_spent_seconds)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (
        data.student_id,
        data.topic_id,
        data.question,
        data.student_answer,
        data.correct_answer,
        is_correct,
        score,
        data.time_spent_seconds
    ))