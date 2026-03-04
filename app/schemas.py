from pydantic import BaseModel

class AnswerSubmission(BaseModel):
    student_id: int
    topic_id: int
    question: str
    student_answer: str
    correct_answer: str
    time_spent_seconds: int
print("Schemas file loaded")