from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import asyncio
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


from resources.resource import RecommendationResource, ReviewResource, UserResource
from model import CoursePrerequisitesRequest, RecommendationRequest, ReviewRequest

# import logging
from fastapi import Request


app = FastAPI()
# logging.basicConfig(level=logging.DEBUG)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

recommendation_instance = RecommendationResource()
review_instance = ReviewResource()
user_instance = UserResource()
logger = logging.getLogger(__name__)


@app.get("/")
async def home_page():
    home_page = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Simple Composite Service Example</title>
        </head>
        <body>
        
            <header>
                <h1>Welcome to Simple Composite Example</h1>
            </header>
        
            <section>
                <h2>Usage</h2>
                <p>Please go to <a href="/docs">the OpenAPI docs page for this app.</a>
            </section>
        
        
        </body>
        </html>
        """
    return HTMLResponse(home_page)


# """Example"""
# @app.get("/get_item")
# async def async_call(item_name: str = None):
#     result = await recommendation_instance.get_item(item_name)
#     return JSONResponse(content={"message": result})

"""SYNC CALLS"""


@app.post("/create_recommendation_by_student")
async def create_recommendation_by_student(email: str):
    # 1. get student history
    # 2. generate recommendation by history
    ok, result = await recommendation_instance.create_recommendation_by_student(email)
    if ok:
        return JSONResponse(content={"message": result})
    else:
        return JSONResponse(content={"message": "fail"})


@app.get("/get_reviews")
async def get_reviews(
    per_page=None,
    page=None,
    review_id=None,
    user_id=None,
    pinned=None,
    course_name=None,
    course_number=None,
    instructor_name=None,
    department=None,
    term=None,
    year=None,
    modes_of_instruction=None,
    overall_rating=None,
    contents=None,
    shown=None,
):
    try:
        # logging.info(request.params)
        ok, result = await review_instance.get_reviews(
            per_page,
            page,
            review_id,
            user_id,
            pinned,
            course_name,
            course_number,
            instructor_name,
            department,
            term,
            year,
            modes_of_instruction,
            overall_rating,
            contents,
            shown,
        )

    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail="Internal Server Error")

    if ok:
        logging.info(result["response_data"])
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.get("/get_unshown_reviews")
async def get_unshown_reviews():
    try:
        ok, result = await review_instance.get_unshown_reviews()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=501, detail="Internal Server Error")

    if ok:
        logging.info(result["response_data"])
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.post("/post_review")
async def post_review(request: Request):
    try:
        data = await request.json()
        ok, result = await review_instance.post_review(data)

    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail="post review Error")

    if ok:
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.put("/update_review")
async def update_review(request: Request):
    try:
        data = await request.json()
        ok, result = await review_instance.update_review(data)

    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail="post review Error")

    if ok:
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.delete("/delete_review")
async def delete_review(request: Request):
    try:
        b = await request.body()
        logging.info(b)
        data = await request.json()
        logging.info(data)
        ok, result = await review_instance.delete_review(data)
        logging.info(data)

    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail="post review Error")

    if ok:
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.get("/get_comments_by_review_id")
async def get_comments_by_review_id(review_id):
    try:
        ok, result = await review_instance.get_comments_by_review_id(review_id)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=501, detail="Internal Server Error")

    if ok:
        logging.info(result["response_data"])
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.get("/get_num_of_likes_by_review_id")
async def get_num_of_likes_by_review_id(review_id):
    try:
        ok, result = await review_instance.get_num_of_likes_by_review_id(review_id)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=501, detail="Internal Server Error")

    if ok:
        logging.info(result["response_data"])
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.get("/get_num_of_dislikes_by_review_id")
async def get_num_of_dislikes_by_review_id(review_id):
    try:
        ok, result = await review_instance.get_num_of_dislikes_by_review_id(review_id)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=501, detail="Internal Server Error")

    if ok:
        logging.info(result["response_data"])
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.post("/post_comment")
async def post_comment(request: Request):
    try:
        data = await request.json()
        ok, result = await review_instance.post_comment(data)

    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail="post comment Error")

    if ok:
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.post("/update_comment")
async def update_comment(request: Request):
    try:
        data = await request.json()
        ok, result = await review_instance.update_comment(data)

    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail="update comment Error")

    if ok:
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


@app.post("/delete_comment")
async def delete_comment(request: Request):
    try:
        data = await request.json()
        ok, result = await review_instance.delete_comment(data)

    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")
        # Raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail="delete comment Error")

    if ok:
        return JSONResponse(content=result["response_data"])
    else:
        return JSONResponse(content={"message": "fail"})


"""ASYNC CALLS"""


@app.post("/check_fufilled_all_course_prerequisites")
async def async_check_fufilled_all_course_prerequisites(
    request: CoursePrerequisitesRequest,
):
    """
    check with the given courses the student can take this course
    """

    result = await recommendation_instance.check_fufilled_all_course_prerequisites(
        request.courses_taken, request.target_courses
    )
    return JSONResponse(content={"message": result})


@app.get("/get_student_taken_courses")
async def get_student_taken_courses(email: str):
    """
    get all the courses that the student has taken
    """
    result = await user_instance.get_student_taken_courses(email)
    return JSONResponse(content={"message": result})


@app.get("/get_student_recommendations")
async def get_student_recommendations(email: str):
    """
    get all the student recommendation records, and student history
    """
    result = await recommendation_instance.get_student(email)
    return JSONResponse(content={"message": result})


######### add/remove courses from student
@app.post("/add_course")
async def add_student_history(
    email: str,
    semester: str,
    track: str = None,
    courseOne: str = None,
    courseTwo: str = None,
    courseThree: str = None,
    courseFour: str = None,
):
    data = {
        "courseOne": courseOne,
        "courseTwo": courseTwo,
        "courseThree": courseThree,
        "courseFour": courseFour,
        "track": track,
        "semester": semester,
    }
    ok = await user_instance.add_semester(email, data)
    if ok:
        return JSONResponse(content={"message": "OK"})
    return JSONResponse(content={"message": "Duplicate"}, status_code=400)
    pass


@app.delete("/remove_course")
async def remove_course(id: str):
    ok = await user_instance.remove_semester(id)
    if ok:
        return JSONResponse(content={"message": "remove OK"})
    return JSONResponse(content={"message": "nooooo"})


@app.put("/update_course")
async def update_course(
    id: str,
    email: str,
    semester: str,
    track: str = None,
    courseOne: str = None,
    courseTwo: str = None,
    courseThree: str = None,
    courseFour: str = None,
):
    data = {
        "courseOne": courseOne,
        "courseTwo": courseTwo,
        "courseThree": courseThree,
        "courseFour": courseFour,
        "track": track,
        "semester": semester,
    }
    ok = await user_instance.update_semester(id, data)
    if ok:
        return JSONResponse(content={"message": "update OK"})
    return JSONResponse(content={"message": "nooooo"})


@app.get("/check_student_course_fufillment")
async def check_student_course_fufillment(email: str, target_course: str):
    """
    check if the student can take this course
    1. get_student_taken_courses
    2. check_fufilled_all_course_prerequisites
    """
    result = await recommendation_instance.check_course_fufillment(email, target_course)
    return JSONResponse(content={"message": result})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8050, log_level="info")
