"""config path"""
import util

class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:yin732501242@localhost/test'
    # nSQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:Natalie3399!@database-1.cvlxq8ccnbut.us-east-1.rds.amazonaws.com:3306/recommendation"
    user_server_ip = "http://localhost:8080"
    recommendation_server_ip = "http://3.144.39.6:5000"
    pass


class Review(object):
    review_server_ip = ""
    get_review = "/api/review/"
    get_reviews = "/api/reviews/"
    get_reviews_by_user = "/api/review/user/"

    # Method to get a review by review-id
    @staticmethod
    def get_review_by_id(review_id):
        return f"{Review.get_review}{review_id}"

    # Method to get reviews (with filters as params)
    @staticmethod
    def get_all_reviews(params=None):
        return Review.get_reviews

    # Method to get all reviews by a specific user
    @staticmethod
    def get_user_reviews(user_id):
        return f"{Review.get_reviews_by_user}{user_id}"

    # Method to post a review
    @staticmethod
    def post_review():
        return "/api/review/"

    # Method to update a review by review_id
    @staticmethod
    def update_review(review_id):
        return f"/api/review/{review_id}"

    # Method to delete a review by review_id
    @staticmethod
    def delete_review(review_id):
        return f"/api/review/{review_id}"

    # Method to get a comment by comment_id
    @staticmethod
    def get_comment_by_id(comment_id):
        return f"/api/review/comment/{comment_id}"

    # Method to get all comments for a review
    @staticmethod
    def get_comments_for_review(review_id):
        return f"/api/review/{review_id}/comment"

    # Method to reply to a review (comment, like, dislike, report, etc.)
    @staticmethod
    def post_comment():
        return "/api/review/comment"

    # Method to update a comment/like/dislike/report by comment id
    @staticmethod
    def update_comment(comment_id):
        return f"/api/review/comment/{comment_id}"

    # Method to delete a comment by comment id
    @staticmethod
    def delete_comment(comment_id):
        return f"/api/review/comment/{comment_id}"

    # Method for admin to pin a review
    @staticmethod
    def pin_review(review_id):
        return f"/api/admin/pin_review/{review_id}"


class UserConfig(object):
    user_server_ip = Config.user_server_ip
    get_student_history_url = "/student_history/get"
    

    @staticmethod
    def get_student_history_by_email(email):
        return f"{UserConfig.user_server_ip}{UserConfig.get_student_history_url}/{email}"


class RecommendationConfig(object):
    recommendation_server_ip = Config.recommendation_server_ip
    get_track_url = "/api/get_track"
    get_course_url = "/api/get_course"
    get_recommendation_url = "/api/get_recommendation"
    create_recommendation_url = "/api/create_recommendation"
    fufilled_course_prerequisites_url = "/api/fufilled_course_prerequisites"
    @staticmethod
    def get_track_by_name(name=""):
        return f"{RecommendationConfig.recommendation_server_ip}{RecommendationConfig.get_track_url}?track_name={name}"

    @staticmethod
    def get_course_by_name(name=""):
        return f"{RecommendationConfig.recommendation_server_ip}{RecommendationConfig.get_course_url}?course_name={name}"

    @staticmethod
    def create_recommendation():
        return f"{RecommendationConfig.recommendation_server_ip}{RecommendationConfig.create_recommendation_url}"
    
    @staticmethod
    def get_recommendation_all(uni):
        return f"{RecommendationConfig.recommendation_server_ip}{RecommendationConfig.get_recommendation_url}?uni={uni}&all=true"
    @staticmethod
    def get_latest_recommendation(uni):
        return f"{RecommendationConfig.recommendation_server_ip}{RecommendationConfig.get_recommendation_url}?uni={uni}"

    @staticmethod
    def check_fufilled_course_prerequisites():
        return f"{RecommendationConfig.recommendation_server_ip}{RecommendationConfig.fufilled_course_prerequisites_url}" 