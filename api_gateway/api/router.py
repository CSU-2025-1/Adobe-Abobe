import logging

from fastapi import APIRouter, HTTPException, UploadFile, File, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from internal.core.entity.auth.auth_dto import AuthRequest
from internal.core.entity.story.story_dto import StoryRequest
from internal.core.entity.upload.upload_dto import UploadRequest
from internal.core.entity.filter.filter_dto import FilterRequest
from internal.broker.rabbitclient.producers import send_authorization_message, send_validate_message, \
    send_filters_message, send_upload_message
from fastapi.responses import JSONResponse

router = APIRouter()
security = HTTPBearer()


# Auth
@router.post("/auth/register")
async def register(data: AuthRequest):
    try:
        command = "register"
        response = await send_authorization_message(data, command)
        return {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/login")
async def login(data: AuthRequest):
    try:
        command = "login"
        response = await send_authorization_message(data, command)
        return {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Upload
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
# async def upload_file(file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Security(security)):

    # token = credentials.credentials
    #
    # auth_validate = await send_validate_message(token)
    #
    # if auth_validate["valid"]:
        try:
            file_data = await file.read()
            logging.info(f"file name: {file.filename}")
            logging.info(f"file ct: {file.content_type}")

            image_data = UploadRequest(
                content=file_data,
                filename=file.filename,
                content_type=file.content_type,
                user_id="111",
            )

            response = await send_upload_message(image_data)
            logging.info(f"[gateway] got response from upload-service: {response}")

            if response["status"] == "success":
                return {
                    "image_id": response["image_id"],
                    "image_url": response["image_url"],
                }
            else:
                raise HTTPException(status_code=500, detail="File upload failed")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    # else:
    #     raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/story")
async def get_user_story(data: StoryRequest, credentials: HTTPAuthorizationCredentials = Security(security)):

    token = credentials.credentials

    auth_validate = await send_validate_message(token)

    if auth_validate["valid"]:
        try:
            response = await send_story_message(data)

            if "detail" in response:
                raise HTTPException(status_code=404, detail=response["detail"])

            if "url" not in response or "filters" not in response:
                raise HTTPException(status_code=500, detail="Некорректный формат ответа от сервиса")

            return JSONResponse(content=response)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка получения истории: {str(e)}")
    else:
        raise HTTPException(status_code=401, detail="Invalid token")


# Edit Photo
@router.post("/editphoto/filter/")
async def apply_filter(data: FilterRequest):
    try:
        response = await send_filters_message(data)
        if not response:
            raise HTTPException(status_code=500, detail="Filter service returned no response")
        return {
            "filtered_url": response["filtered_url"],
            "timestamp": response["timestamp"],
            "filters": response["filters"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")


# @router.post("/editphoto/filter")
# async def apply_filter(data: FilterRequest, credentials: HTTPAuthorizationCredentials = Security(security)):
#
#     token = credentials.credentials
#
#     auth_validate = await send_validate_message(token)
#
#     if auth_validate["valid"]:
#         try:
#             response = await send_filters_message(data)
#             return {
#                 "filtered_url": response["filtered_url"]
#             }
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"error: {str(e)}")
#     else:
#         raise HTTPException(status_code=401, detail="Invalid token")
