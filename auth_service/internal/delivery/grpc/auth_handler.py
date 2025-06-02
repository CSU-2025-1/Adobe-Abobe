# from api.auth import auth_pb2, auth_pb2_grpc
# import bcrypt, jwt
# import os
#
# from config.config import config
#
# SECRET = os.getenv("JWT_SECRET", config.jwt_secret)
#
# class AuthService(auth_pb2_grpc.AuthServiceServicer):
#     def __init__(self, pg_repo, redis_repo):
#         self.pg = pg_repo
#         self.redis = redis_repo
#
#     def Register(self, request, context):
#         password_hash = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
#         user_id = self.pg.create_user(request.login, password_hash)
#         return self._generate_tokens(user_id)
#
#     def Login(self, request, context):
#         user = self.pg.get_user_by_login(request.login)
#         if not user or not bcrypt.checkpw(request.password.encode(), user[1].encode()):
#             context.abort(401, "Invalid credentials")
#         return self._generate_tokens(user[0])
#
#     def ValidateToken(self, request, context):
#         print(f"Received access token: {request.access_token} (type: {type(request.access_token)})")
#
#         if request.access_token is None:
#             context.abort(400, "Access token is missing")
#
#         if not isinstance(request.access_token, str):
#             context.abort(400, "Invalid access token format")
#
#         try:
#             payload = jwt.decode(request.access_token, SECRET, algorithms=["HS256"])
#             user_id = str(payload["user_id"])
#             return auth_pb2.ValidateResponse(valid=True, user_id=user_id)
#         except jwt.ExpiredSignatureError:
#             return auth_pb2.ValidateResponse(valid=False, user_id="SIGNATURE_ERROR")
#         except jwt.InvalidTokenError as e:
#             print(f"Invalid token error: {e}")
#             return auth_pb2.ValidateResponse(valid=False, user_id="INVALID_TOKEN")
#         except Exception as exception:
#             print(f"Unexpected error: {exception}")
#             return auth_pb2.ValidateResponse(valid=False, user_id=str(exception))
#
#     def _generate_tokens(self, user_id):
#         access_token = jwt.encode({"user_id": user_id}, SECRET, algorithm="HS256")
#         refresh_token = jwt.encode({"user_id": user_id, "type": "refresh"}, SECRET, algorithm="HS256")
#         self.redis.set_refresh_token(user_id, refresh_token)
#         return auth_pb2.AuthResponse(access_token=access_token, refresh_token=refresh_token)