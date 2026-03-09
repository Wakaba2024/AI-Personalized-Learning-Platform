# Average Score Per Student

def average_score_per_student(cur):

    cur.execute("""
        SELECT student_id,
               ROUND(AVG(score),2) AS avg_score,
               COUNT(*) AS quizzes_taken
        FROM quiz_results
        GROUP BY student_id
        ORDER BY avg_score DESC
    """)

    return cur.fetchall()

# Average Score Per Topic (Reveals the hardest topics)

def average_score_per_student(cur):

    cur.execute("""
        SELECT student_id,
               ROUND(AVG(score),2) AS avg_score,
               COUNT(*) AS quizzes_taken
        FROM quiz_results
        GROUP BY student_id
        ORDER BY avg_score DESC
    """)

    return cur.fetchall()

# Performance Trend Over Time (Informs teachers whether students are improving over time)

def average_score_per_topic(cur):

    cur.execute("""
        SELECT t.topic_name,
               ROUND(AVG(q.score),2) AS avg_score,
               COUNT(*) AS attempts
        FROM quiz_results q
        JOIN topics t
        ON q.topic_id = t.topic_id
        GROUP BY t.topic_name
        ORDER BY avg_score ASC
    """)

    return cur.fetchall()

# Identify Students Below 50% (Teachers can detect students who need help)

def performance_trend(cur):

    cur.execute("""
        SELECT DATE(created_at) AS date,
               ROUND(AVG(score),2) AS avg_score,
               COUNT(*) AS quizzes_taken
        FROM quiz_results
        GROUP BY DATE(created_at)
        ORDER BY date
    """)

    return cur.fetchall()

# At-risk student prediction

# Prediction Rule
# Avg Score < 40 And at least 3 quizzes

def at_risk_students(cur):

    cur.execute("""
        SELECT student_id,
               COUNT(*) AS quizzes_taken,
               ROUND(AVG(score),2) AS avg_score
        FROM quiz_results
        GROUP BY student_id
        HAVING AVG(score) < 40
        AND COUNT(*) >= 3
    """)

    return cur.fetchall()

# Average Time Spent Per Topic
# The interpretation is that a higher time is equal to a higher topic

def at_risk_students(cur):

    cur.execute("""
        SELECT student_id,
               COUNT(*) AS quizzes_taken,
               ROUND(AVG(score),2) AS avg_score
        FROM quiz_results
        GROUP BY student_id
        HAVING AVG(score) < 40
        AND COUNT(*) >= 3
    """)

    return cur.fetchall()

# Performance Query

def student_topic_performance(cur, student_id):

    cur.execute("""
        SELECT t.topic_name,
               ROUND(AVG(q.score),2) AS avg_score
        FROM quiz_results q
        JOIN topics t
        ON q.topic_id = t.topic_id
        WHERE q.student_id = %s
        GROUP BY t.topic_name
    """, (student_id,))

    return cur.fetchall()