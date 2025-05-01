from fastapi import APIRouter, Query, HTTPException, UploadFile, File
from internal.core.entity.auth import AuthRequest
from internal.core.entity.upload import UploadRequest
from lib.rabbitclient.producers import send_auth_message, send_authorization_message, send_image_message

router = APIRouter()


# Auth
@router.post("/auth/register")
async def register(data: AuthRequest):
    try:
        response = await send_authorization_message(data)
        return {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/login")
async def login(data: AuthRequest):
    try:
        response = await send_authorization_message(data)
        return {
            "access_token": response["access_token"],
            "refresh_token": response["refresh_token"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Upload / Download
@router.post("/upload")
async def upload_file(token: str, file: UploadFile = File(...)):
    auth_validate = await send_auth_message(token)

    if auth_validate["valid"]:
        try:
            file_data = await file.read()

            image_data = UploadRequest(
                content=file_data,
                filename=file.filename,
                content_type=file.content_type,
                user_id=auth_validate["user_id"],
            )

            response = await send_image_message(image_data)

            if response["status"] == "success":
                return {
                    "image_id": response["image_id"],
                }
            else:
                raise HTTPException(status_code=500, detail="File upload failed")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    else:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/download")
async def download_file(token: str, image_id: int):
    auth_validate = await send_auth_message(token)

    if auth_validate["valid"]:
        pass
    else:
        raise HTTPException(status_code=401, detail="Invalid token")


# Edit Photo
@router.post("/editphoto/filter/{filter_id}")
async def edit_photo_with_param(filter_id: str, param: str = Query(...)):
    pass


@router.post("/editphoto/filter/{filter_id}")
async def edit_photo_null_param(filter_id: str):
    pass


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
