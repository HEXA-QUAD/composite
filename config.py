"""config path"""
import util
# import logging
# logging.basicConfig(level=logging.DEBUG)

class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:yin732501242@localhost/test'
    # nSQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:Natalie3399!@database-1.cvlxq8ccnbut.us-east-1.rds.amazonaws.com:3306/recommendation"
    user_server_ip = "https://project-405004.ue.r.appspot.com"
    recommendation_server_ip = "http://3.144.39.6:5000"
    review_server_ip = "http://ec2-3-88-202-217.compute-1.amazonaws.com:8080"
    pass


class ReviewConfig(object):
    review_server_ip = Config.review_server_ip
    review_url = "/api/review"
    comment_url = "/api/review/comment"
    admin_url = "/api/admin"


    # Method to get reviews (with filters as params)
    @staticmethod
    def get_reviews(review_id, user_id, pinned, course_name, course_number, instructor_name, department, term, year, modes_of_instruction, overall_rating, contents, show):
        parameters = locals()
        return_f = f"{ReviewConfig.review_server_ip}{ReviewConfig.review_url}"

        # Iterate through the parameters
        flag = False
        for key, value in parameters.items():
            if value == None:
                continue
            if flag == False:
                return_f += f"?{key}={value}"
                flag = True
            else:
                return_f += f"&{key}={value}"
        # logging.info(return_f)
        return return_f
    
    # Method to get all unshowed reviews
    @staticmethod
    def get_unshown_reviews():
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.review_url}?shown=0"

    # Method to post a review
    @staticmethod
    def post_review():
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.review_url}"

    # Method to update a review by review_id
    @staticmethod
    def update_review():
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.review_url}"

    # Method to delete a review by review_id
    @staticmethod
    def delete_review():
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.review_url}"

    # Method to get a comment by comment_id
    @staticmethod
    def get_comment_by_id(comment_id):
        # not yet implemented
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.comment_url}?comment_id={comment_id}"

    # Method to get all comments for a review
    @staticmethod
    def get_comments_for_review(review_id):
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.comment_url}?review_id={review_id}&type=comment"

    # Method to get the number of likes for a review
    @staticmethod
    def get_num_of_likes_for_review(review_id):
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.comment_url}/like/"
    
    # Method to get the number of dislikes for a review
    @staticmethod
    def get_num_of_dislikes_for_review(review_id):
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.comment_url}/dislike/"

    # Method to reply to a review (comment, like, dislike, report, etc.)
    @staticmethod
    def post_comment():
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.comment_url}"

    # Method to update a comment/like/dislike/report by comment id
    @staticmethod
    def update_comment():
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.comment_url}"

    # Method to delete a comment by comment id
    @staticmethod
    def delete_comment(comment_id):
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.comment_url}"

    # Method for admin to pin a review
    @staticmethod
    def pin_review(review_id):
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.admin_url}/pin_review"

    # Method for admin to unpin a review
    @staticmethod
    def unpin_review(review_id):
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.admin_url}/unpin_review"

    # Method for admin to show a review
    @staticmethod
    def show_review(review_id):
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.admin_url}/show_review"
    
    # Method for admin to hide a review
    @staticmethod
    def hide_review(review_id):
        return f"{ReviewConfig.review_server_ip}{ReviewConfig.admin_url}/hide_review"

class UserConfig(object):
    user_server_ip = Config.user_server_ip
    student_history_url = "/student_history"

    @staticmethod
    def get_student_history_by_email(email):
        return f"{UserConfig.user_server_ip}{UserConfig.student_history_url}/get/{email}"

    @staticmethod
    def add_student_history_by_email(email):
        return f"{UserConfig.user_server_ip}{UserConfig.student_history_url}/add/{email}"
    
    @staticmethod
    def delete_student_history(id):
        return f"{UserConfig.user_server_ip}{UserConfig.student_history_url}/{id}"

    @staticmethod
    def update_student_history_by_email(id):
        return f"{UserConfig.user_server_ip}{UserConfig.student_history_url}/update/{id}"


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