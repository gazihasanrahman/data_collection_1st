import os
import json
import boto3
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn
import config
from utils.logger import logger_1st
from functools import wraps


# configs
app = FastAPI(title="Data Collection API", version="1.0.0")
security = HTTPBearer()
api_key = os.getenv("TPD_API_KEY")
sqs_client = boto3.client('sqs')


# Global exception handler for all unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger_1st.error(f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": "Internal server error"}
    )


# HTTP exception handler for FastAPI HTTPExceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger_1st.warning(f"HTTP {exc.status_code} on {request.method} {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail}
    )


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    if credentials.credentials != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/1st-data")
async def receive_1st_data(data: Dict[str, Any]):
    """Endpoint for 1st-data without authentication - IP whitelisted at ALB level"""
    try:
        sqs_client.send_message(QueueUrl=config.SQS_QUEUE_URL, MessageBody=json.dumps(data))
        return {"status": "success"}
    except Exception as e:
        logger_1st.error(f"Error in received 1st-data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/{path:path}")
async def receive_data(path: str, data: Dict[str, Any], api_key_verified: bool = Depends(verify_api_key)):
    """General endpoint for other paths with authentication"""
    try:
        # Skip 1st-data as it has its own endpoint
        if path == "1st-data":
            raise HTTPException(status_code=404, detail="Invalid path")
            
        # Handle other authenticated paths here
        match path:
            case _:
                raise HTTPException(status_code=404, detail="Invalid path")

    except Exception as e:
        logger_1st.error(f"Error in received data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(app, 
                host=config.TPD_API_HOST, 
                port=config.TPD_API_PORT, 
                reload=config.TPD_API_RELOAD
                )
