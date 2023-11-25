# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.hashers import check_password
# from django.db import connection
# from .models import User  # Import your User model

# class UserTypeAuthBackend(ModelBackend):
#     #user_class = User  # Use your custom User model
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         cursor = connection.cursor()

#         # Customize the SQL query based on your actual user model
#         #print([username, password, kwargs.get('user_type')])
#         query = """
#             SELECT * FROM vaccine_user
#             WHERE user_name = %s AND password = %s AND user_type = %s
#         """

#         cursor.execute(query, [username, password, kwargs.get('user_type')])
#         user_row = cursor.fetchone()
#         print(user_row)

#         if user_row:
#             # Create a user instance from the row data
#             #user = self.user_class.from_db(None, user_row)
#             #user = self.user_class()
#             auser = User.from_db(None,None,user_row)
#             return auser

#             # # Check the password
#             # if check_password(password, user.password):
                

#         return None