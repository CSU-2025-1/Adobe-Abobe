import logging

from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Header, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from internal.core.entity.auth.auth_dto import AuthRequest
from internal.core.entity.upload.upload_dto import UploadRequest
from internal.core.entity.filter.filter_dto import FilterRequest
from internal.broker.rabbitclient.producers import send_authorization_message, send_validate_message, \
    send_filters_message, send_upload_message

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


# Upload / Download
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Security(security)):

    token = credentials.credentials

    auth_validate = await send_validate_message(token)

    if auth_validate["valid"]:
        try:
            file_data = await file.read()
            logging.info(f"file name: {file.filename}")
            logging.info(f"file ct: {file.content_type}")

            image_data = UploadRequest(
                content=file_data,
                filename=file.filename,
                content_type=file.content_type,
                user_id=f"{auth_validate["user_id"]}",
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
    else:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/download")
async def download_file(token: str, image_id: int):
    auth_validate = await send_validate_message(token)

    if auth_validate["valid"]:
        pass
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
"""
@router.post("/editphoto/filter/")
async def apply_filter(token: str, data: FilterRequest):
    auth_validate = await send_validate_message(token)

    if auth_validate["valid"]:
        try:
            response = await send_filters_message(data)
            return {
                "filtered_url": response["filtered_url"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
"""


# VCS
@router.get("/vcs/forward")
async def vcs_forward(version: str = Query(...)):
    pass


@router.get("/vcs/backward")
async def vcs_backward():
    pass


@router.post("/vcs")
async def vcs_save():
    pass
