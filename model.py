from pydantic import BaseModel
from typing import List

class CoursePrerequisitesRequest(BaseModel):
    courses_taken: List[str]
    target_courses: List[str]



class RecommendationRequest(BaseModel):
    email: str