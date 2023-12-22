from pydantic import BaseModel
from typing import List, Dict, Any

class CoursePrerequisitesRequest(BaseModel):
    courses_taken: List[str]
    target_courses: List[str]




class RecommendationRequest(BaseModel):
    email: str

class ReviewRequest(BaseModel):
    review_id: int
    user_id: str
    pinned: bool
    course_name: str
    course_number: str
    instructor_name: str
    department: str
    term: str
    year: int
    modes_of_instruction: str
    overall_rating: int
    contents: str
    show: bool

class CommentRequest(BaseModel):
    comment_id: int
    review_id: int
    type: str
    contents: str
    user_id: str