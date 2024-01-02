from fastapi import FastAPI, Depends, Request, Response
from sqlalchemy.orm import Session

from app.models import FunctionBase
from app.db import SessionLocal, add_function

# Create FastAPI instance
app = FastAPI()


# Middleware for handling db sessions
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.post("/functions/")
def submit_function(function: FunctionBase, request: Request):
    db = request.state.db
    return add_function(db, function)
