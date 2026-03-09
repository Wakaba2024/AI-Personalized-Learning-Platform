from mistralai import Mistral
from app.settings import settings

client = Mistral(api_key=settings.MISTRAL_API_KEY)


# Generate Quiz Questions

def generate_quiz(topic, difficulty):

    prompt = f"""
Create one quiz question about {topic}.

Difficulty: {difficulty}

Return the answer strictly in this format:

Question:
Option A:
Option B:
Option C:
Option D:
Correct Answer:
Explanation:
"""

    response = client.chat.complete(
        model="mistral-small",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Generate AI Feedback and Students receive explanations after answering.

def generate_feedback(question, student_answer, correct_answer):

    prompt = f"""
    Question: {question}

    Student Answer: {student_answer}

    Correct Answer: {correct_answer}

    Explain whether the student is correct.
    Give a short explanation.
    """

    response = client.chat.complete(
        model="mistral-small",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# Simplified Explanations (Accessibility) this supports students with cognitive challenges.

def simplify_explanation(topic):

    prompt = f"""
    Explain {topic} in very simple language.

    Use:
    - short sentences
    - simple words
    - examples
    """

    response = client.chat.complete(
        model="mistral-small",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# Recommendation Function

def generate_learning_recommendation(topic, avg_score):

    prompt = f"""
A student has an average score of {avg_score}% in {topic}.

Provide learning advice for the student.

If the score is low:
Suggest reviewing basic concepts and practicing easier problems.

If the score is moderate:
Suggest more practice problems.

If the score is high:
Suggest more advanced challenges.

Give a short explanation suitable for a student.
"""

    response = client.chat.complete(
        model="mistral-small",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content