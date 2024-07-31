import os
from mangum import Mangum
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from starlette import status
from common import constant
from common.logger_utils import get_logger
from common.schemas import Error
from common.exception_handler import biz_exception

from pet.main import router as pet_router

logger = get_logger(constant.LOGGER_API)

X_API_KEY_HEADER = APIKeyHeader(name='X-API-Key')
X_API_KEY = os.getenv('X-API-Key','1234')


def check_authentication_header(x_api_key: str = Depends(X_API_KEY_HEADER)):
    if x_api_key != X_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )

stage = os.getenv('Stage')
root_path = f"/{stage}" if stage else ""
logger.info(f"root_path={root_path}")
app = FastAPI(title="Video Editing based on Video Understanding",
              version="v0.1.0",
              dependencies=[Security(check_authentication_header)],
              responses={
                  status.HTTP_400_BAD_REQUEST:{"model":Error},
                  status.HTTP_403_FORBIDDEN:{},
              },
              root_path=root_path,
              )
biz_exception(app)

app.include_router(pet_router)
handler = Mangum(app)