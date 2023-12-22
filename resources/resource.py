from pydantic import BaseModel
import asyncio
import aiohttp
import json
import time
import requests
from config import RecommendationConfig, UserConfig, ReviewConfig
import util
from typing import Dict, Any
import logging
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class Recommendation(BaseModel):
    name: str


class RecommendationResource:
    resources = [
        {"resource": "get_all_track", "url": RecommendationConfig.get_course_by_name()},
        {"resource": "get_all_course", "url": RecommendationConfig.get_track_by_name()},
        {"resource": "get_all_course", "url": RecommendationConfig.get_track_by_name()},
    ]

    async def get_item(self, item: Recommendation = None, sleep=5) -> str:
        # Simulate an asynchronous operation
        print(item, "ittttt")
        if item and item.name:
            n = item.name
        else:
            n = "Item with no name."
        await asyncio.sleep(sleep)
        return f"Hello, {n}! This is an asynchronous response."

    @classmethod
    async def handle_response(cls, response):
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return await response.json()
        else:
            # If not JSON, read the response as text
            return {"error": "Non-JSON response", "content": await response.text()}

    @classmethod
    async def fetch(cls, session, resource, method="GET", data=None):
        start_time = time.time()  # Start timing
        status_code = None

        url = resource["url"]
        print("Calling URL =", url, "Method =", method)

        if method.upper() == "GET":
            async with session.get(url) as response:
                status_code = response.status
                response_data = await cls.handle_response(response)
        elif method.upper() == "DELETE":
            async with session.delete(url) as response:
                status_code = response.status
                response_data = await cls.handle_response(response)
        elif method.upper() == "PUT":
            async with session.put(url, json=data) as response:
                status_code = response.status
                response_data = await cls.handle_response(response)
        else:
            async with session.post(url, json=data) as response:
                status_code = response.status
                response_data = await cls.handle_response(response)

        end_time = time.time()  # End timing
        fetch_time = end_time - start_time  # Calculate fetch time
        new_response_data = {"response_data": response_data, "fetch_time": fetch_time}
        result = {
            "status_code": status_code,
            "resource": resource["resource"],
            "data": new_response_data,
            "fetch_time": fetch_time,  # Include fetch time in the result
        }
        logger.info(f"URL {url} returned {str(response_data)} in {fetch_time} seconds\n\n")
        return result

    # sync
    async def create_recommendation_by_student(self, email: str):
        get_student_history_resource = {
            "resource": "get_student_history",
            "url": UserConfig.get_student_history_by_email(email),
        }
        create_recommendation_resource = {
            "resource": "create_recommendation",
            "url": RecommendationConfig.create_recommendation(),
        }

        async with aiohttp.ClientSession() as session:
            # Fetch student history
            student_history_response = await self.fetch(
                session, get_student_history_resource
            )
            student_history = student_history_response["data"]["response_data"]
            if not student_history:
                return False, "No student history found"

            courses_taken = set()
            for history in student_history:
                courses_taken.update(
                    [
                        history.get("courseOne"),
                        history.get("courseTwo"),
                        history.get("courseThree"),
                        history.get("courseFour"),
                    ]
                )
            courses_taken.remove(None)
            recommendation_data = {
                "uni": util.get_email_name(email),
                "courses_taken": list(courses_taken),
                "track_name": util.get_most_recent_track(student_history),
            }

            # Create a recommendation
            recommendation_response = await self.fetch(
                session,
                create_recommendation_resource,
                method="POST",
                data=recommendation_data,
            )
            recommendation = recommendation_response["data"]

            if recommendation:
                return True, recommendation
            else:
                return False, "Failed to create recommendation"

    # async
    async def check_fufilled_all_course_prerequisites(
        self, courses_taken, target_courses
    ):
        print("heres")
        resources = [
            {
                "resource": f"check_fufilled_course_{t}",
                "url": RecommendationConfig.check_fufilled_course_prerequisites(),
                "target_course": t,
            }
            for i, t in enumerate(target_courses)
        ]

        full_result = None
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(
                    RecommendationResource.fetch(
                        session,
                        res,
                        method="POST",
                        data={
                            "courses_taken": courses_taken,
                            "target_course": res["target_course"],
                        },
                    )
                )
                for res in resources
            ]
            responses = await asyncio.gather(*tasks)
            full_result = {}
            for response in responses:
                full_result[response["resource"]] = response["data"]
            end_time = time.time()
            full_result["elapsed_time"] = end_time - start_time
            return full_result
            # print("\nFull Result = ", json.dumps(full_result, indent=2))

    # async
    async def get_student(self, email: str):
        """Get student history and its all recommendations"""
        resources = [
            {
                "resource": "get_student_history",
                "url": UserConfig.get_student_history_by_email(email),
            },
            {
                "resource": "get_student_all_recommendation",
                "url": RecommendationConfig.get_recommendation_all(
                    util.get_email_name(email)
                ),
            },
        ]
        full_result = None
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(
                    RecommendationResource.fetch(
                        session,
                        res,
                    )
                )
                for res in resources
            ]
            responses = await asyncio.gather(*tasks)
            full_result = {}
            for response in responses:
                full_result[response["resource"]] = response["data"]
            end_time = time.time()
            full_result["total_elapsed_time"] = end_time - start_time
        return full_result

    async def check_course_fufillment(self, email: str, target_course):
        user_instance = UserResource()

        r1 = await user_instance.get_student_taken_courses(
            email
        )  # ['message']['get_student_history']
        taken_courses = r1.get("get_student_history")
        r2 = await self.check_fufilled_all_course_prerequisites(
            taken_courses, [target_course]
        )  # ['msg']

        fufillment = r2.get(f"check_fufilled_course_{target_course}")["response_data"][
            "msg"
        ]
        full_result = {}
        full_result["msg"] = False
        if fufillment == "Fufilled":
            full_result["msg"] = True
        return full_result


class ReviewResource:
    async def get_item(self, item: Recommendation = None, sleep=5) -> str:
        # Simulate an asynchronous operation
        print(item, "ittttt")
        if item and item.name:
            n = item.name
        else:
            n = "Item with no name."
        await asyncio.sleep(sleep)
        return f"Hello, {n}! This is an asynchronous response."

    @classmethod
    async def handle_response(cls, response):
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return await response.json()
        else:
            # If not JSON, read the response as text
            return {"error": "Non-JSON response", "content": await response.text()}

    @classmethod
    async def fetch(cls, session, resource, method="GET", data=None):
        start_time = time.time()  # Start timing
        status_code = None

        url = resource["url"]
        print("Calling URL =", url, "Method =", method)
        print(type(data))
        if method.upper() == "GET":
            async with session.get(url) as response:
                status_code = response.status
                response_data = await cls.handle_response(response)
        elif method.upper() == "DELETE":
            async with session.delete(url, json=data) as response:
                status_code = response.status
                response_data = await cls.handle_response(response)
        elif method.upper() == "PUT":
            async with session.put(url, json=data) as response:
                status_code = response.status
                response_data = await cls.handle_response(response)
        else:
            async with session.post(url, json=data) as response:
                status_code = response.status
                response_data = await cls.handle_response(response)

        end_time = time.time()  # End timing
        fetch_time = end_time - start_time  # Calculate fetch time
        new_response_data = {"response_data": response_data, "fetch_time": fetch_time}
        result = {
            "status_code": status_code,
            "resource": resource["resource"],
            "data": new_response_data,
            "fetch_time": fetch_time,  # Include fetch time in the result
        }
        logger.info(f"URL {url} returned {str(response_data)} in {fetch_time} seconds\n\n")
        return result

    # sync
    async def get_reviews(self, review_id, user_id, pinned, course_name, course_number, instructor_name, department, term, year, modes_of_instruction, overall_rating, contents, show):
        try:
            get_reviews_resource = {
                "resource": "get_reviews",
                "url": ReviewConfig().get_reviews(review_id, user_id, pinned, course_name, course_number, instructor_name, department, term, year, modes_of_instruction, overall_rating, contents, show),
            }
            # logging.info(get_reviews_resource["url"])
        except Exception as e:
            # Log the exception
            logging.error(f"An error occurred here: {e}")
            # Raise an HTTPException with a 500 status code
            raise HTTPException(status_code=500, detail="Internal Server Error")

        # return get_reviews_resource["url"]
        # logging.info("sossss")
        async with aiohttp.ClientSession() as session:
            get_reviews_response = await self.fetch(
                session, get_reviews_resource, method="GET"
            )
            get_reviews = get_reviews_response["data"]

            if get_reviews:
                return True, get_reviews
            else:
                return False, f"No review found"    
    async def get_unshown_reviews(self):
        try:
            get_reviews_resource = {
                "resource": "get_unshown_reviews",
                "url": ReviewConfig().get_unshown_reviews(),
            }
            logging.info("here")
        except Exception as e:
            logging.error(f"An error occurred here: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

        async with aiohttp.ClientSession() as session:
            get_reviews_response = await self.fetch(
                session, get_reviews_resource, method="GET"
            )
            get_reviews = get_reviews_response["data"]

            if get_reviews:
                return True, get_reviews
            else:
                return False, f"No review found"
    async def post_review(self, data):
        try:
            post_review_resource = {
                "resource": "get_reviews",
                "url": ReviewConfig().post_review(),
            }
            
        except Exception as e:
            # Log the exception
            logging.error(f"An error occurred here: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

        # return get_reviews_resource["url"]
        async with aiohttp.ClientSession() as session:
            post_review_response = await self.fetch(
                session, post_review_resource, method="POST", data=data
            )
            post_review = post_review_response["data"]

            if post_review:
                return True, post_review
            else:
                return False, f"Post review failed"
    async def update_review(self, data):
        try:
            update_review_resource = {
                "resource": "update_review",
                "url": ReviewConfig().update_review(),
            }
            
        except Exception as e:
            # Log the exception
            logging.error(f"An error occurred here: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

        async with aiohttp.ClientSession() as session:
            update_review_response = await self.fetch(
                session, update_review_resource, method="PUT", data=data
            )
            update_review = update_review_response["data"]

            if update_review:
                return True, update_review
            else:
                return False, f"Update review failed"
    async def delete_review(self, data):
        try:
            delete_review_resource = {
                "resource": "udelete_review",
                "url": ReviewConfig().delete_review(),
            }
            
        except Exception as e:
            # Log the exception
            logging.error(f"An error occurred here: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

        async with aiohttp.ClientSession() as session:
            delete_review_response = await self.fetch(
                session, delete_review_resource, method="DELETE", data=data
            )
            delete_review = delete_review_response["data"]

            if delete_review:
                return True, delete_review
            else:
                return False, f"delete review failed"
class UserResource:
    async def get_student_taken_courses(self, email: str):
        resources = [
            {
                "resource": "get_student_history",
                "url": UserConfig.get_student_history_by_email(email),
            }
        ]
        full_result = None
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(
                    RecommendationResource.fetch(
                        session,
                        res,
                    )
                )
                for res in resources
            ]
            responses = await asyncio.gather(*tasks)
            full_result = {}
            for response in responses:
                temp = set()
                for item in response["data"]["response_data"]:
                    item_1 = item.get("courseOne")
                    item_2 = item.get("courseTwo")
                    item_3 = item.get("courseThree")
                    item_4 = item.get("courseFour")
                    temp.add(item_1) if item_1 else None
                    temp.add(item_2) if item_2 else None
                    temp.add(item_3) if item_3 else None
                    temp.add(item_4) if item_4 else None

                # print(set, "test")
                full_result[response["resource"]] = list(temp)
            end_time = time.time()
            full_result["total_elapsed_time"] = end_time - start_time
        return full_result

    async def add_semester(
        self,
        # semester,
        email,
        data,
    ):
        resource = {
            "resource": "add_student_history",
            "url": UserConfig.add_student_history_by_email(email),
        }
        async with aiohttp.ClientSession() as session:
            response = await RecommendationResource.fetch(
                session,
                resource,
                method="POST",
                data=data,
            )
            print(response)
            if response["status_code"] == 200:
                return True
        return False
    
    async def remove_semester(self, id):
        resource = {
            "resource": "delete_student_history",
            "url": UserConfig.delete_student_history(id),
        }
        async with aiohttp.ClientSession() as session:
            response = await RecommendationResource.fetch(
                session,
                resource,
                method="DELETE",
            )
            if response["status_code"] == 200:
                return True
        return False

    async def update_semester(self, id,data):
        resource = {
            "resource": "delete_student_history",
            "url": UserConfig.delete_student_history(id),
        }
        async with aiohttp.ClientSession() as session:
            response = await RecommendationResource.fetch(
                session,
                resource,
                method="PUT",
                data=data
            )
            if response["status_code"] == 200:
                return True
        return False