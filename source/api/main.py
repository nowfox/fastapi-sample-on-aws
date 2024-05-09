import os
from mangum import Mangum
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from starlette import status
from pet.main import router as pet_router

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

app = FastAPI(title="FastAPI Sample on AWS",
              version="v0.1.0",
              dependencies=[Security(check_authentication_header)],
              responses={403:{"detail":"Not authenticated"}},
              root_path=root_path,
              # servers=[
              #     {"url": "https://{region}.example.com", "description": "Staging environment","variables":{"region":{"default":"ccc","description":"ddd"}}},
              #     {"url": "https://prod.example.com", "description": "Production environment"},
              # ],
              )

app.include_router(pet_router)
handler = Mangum(app)