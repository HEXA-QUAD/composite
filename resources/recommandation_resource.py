from pydantic import BaseModel
import asyncio
import aiohttp
import json
import time
import requests
from config import RecommendationConfig, UserConfig
import util


class Recommendation(BaseModel):
    name: str


class RecommendationResource:
    # resources = [
    #     {"resource": "get_all_track", "url": RecommendationConfig.get_course_by_name()},
    #     {"resource": "get_all_course", "url": RecommendationConfig.get_track_by_name()},
    #     {"resource": "get_all_course", "url": RecommendationConfig.get_track_by_name()},
    # ]

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

        url = resource["url"]
        print("Calling URL =", url, "Method =", method)

        if method.upper() == "POST":
            async with session.post(url, json=data) as response:
                response_data = await cls.handle_response(response)
        else:  # Default to GET if not specified
            async with session.get(url) as response:
                response_data = await cls.handle_response(response)

        end_time = time.time()  # End timing
        fetch_time = end_time - start_time  # Calculate fetch time
        new_response_data = {"response_data": response_data, "fetch_time": fetch_time}
        result = {
            "resource": resource["resource"],
            "data": new_response_data,
            "fetch_time": fetch_time,  # Include fetch time in the result
        }
        print(f"URL {url} returned {str(response_data)} in {fetch_time} seconds\n\n")
        return result

    # async def get_track_course_async(self):
    #     full_result = None
    #     start_time = time.time()
    #     async with aiohttp.ClientSession() as session:
    #         tasks = [
    #             asyncio.ensure_future(RecommendationResource.fetch(session, res))
    #             for res in RecommendationResource.resources
    #         ]
    #         responses = await asyncio.gather(*tasks)
    #         full_result = {}
    #         for response in responses:
    #             full_result[response["resource"]] = response["data"]
    #         end_time = time.time()
    #         full_result["elapsed_time"] = end_time - start_time

    #         return full_result

    #         # print("\nFull Result = ", json.dumps(full_result, indent=2))

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
            student_history = student_history_response["data"]

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

    # sync
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
