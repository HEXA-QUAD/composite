from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import asyncio
import uvicorn
import httpx

from resources.recommandation_resource import RecommendationResource
from model import CoursePrerequisitesRequest, RecommendationRequest

app = FastAPI()


recommendation_instance = RecommendationResource()


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
async def create_recommendation_by_student(request: RecommendationRequest):
    # 1. get student history
    # 2. generate recommendation by history
    ok, result = await recommendation_instance.create_recommendation_by_student(request.email)
    if ok:
        return JSONResponse(content={"message": result})
    else:
        return JSONResponse(content={"message": "fail"})


@app.get("/check_fufilled_all_course_prerequisites")
async def sync_check_fufilled_all_course_prerequisites(
    request: CoursePrerequisitesRequest,
):
    result = await recommendation_instance.check_fufilled_all_course_prerequisites(
        request.courses_taken, request.target_courses
    )
    return JSONResponse(content={"message": result})


"""ASYNC CALLS"""


@app.get("/get_student")
async def async_call_get_student(email: str):
    result = await recommendation_instance.get_student(email)
    return JSONResponse(content={"message": result})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8050, log_level="info")
