import os
import json
import boto3
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import config
from utils.logger import logger_1st
from functools import wraps


# configs
app = FastAPI(title="Data Collection API", version="1.0.0")
security = HTTPBearer()
api_key = os.getenv("TPD_API_KEY")
sqs_client = boto3.client('sqs')


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    if credentials.credentials != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


@app.post("/{path:path}")
async def receive_data(path: str, data: Dict[str, Any], api_key_verified: bool = Depends(verify_api_key)):
    try:
        match path:
            case "1st-data":
                sqs_client.send_message(QueueUrl=config.SQS_QUEUE_URL, MessageBody=json.dumps(data))
                return {"status": "success"}
            case "health":
                return {"status": "healthy"}
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
