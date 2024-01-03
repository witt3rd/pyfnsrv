from fastapi import FastAPI, Depends, Request, Response
from sqlalchemy.orm import Session

from app.models import FunctionSubmission, FunctionExecution
from app.db import SessionLocal, add_function, get_function
from app.exec import execute_code, install_dependencies

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
def submit_function(function: FunctionSubmission, request: Request):
    db = request.state.db
    fn = add_function(db, function)
    install_dependencies(fn.dependencies_list)
    return fn


@app.post("/execute/")
def execute_function(function: FunctionExecution, request: Request):
    db = request.state.db
    fn = get_function(db, function.name)
    exec_result = execute_code(fn.code, fn.name, function.args)
    return exec_result
