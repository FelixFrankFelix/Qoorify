from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List,Union
#from model.request import UserRequest
#from model.response import UserResponse
#from repository.database import UserRepository
from db import SessionLocal, engine
from utility.exceptions import ResponseConstant
from schemas import ResponseUnionSession,SessionRequest,ResponseUnionSessions,SessionUpdateRequest,ResponseUnionVerifications,ResponseUnionVerification,Verification,VerificationUpdateRequest,DetailedResponseSessions,UserSessions,SessionResponse,Sessions
import repository
import service
from sqlalchemy.inspection import inspect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-session/", response_model=ResponseUnionSession)
def create_session_controller(session: SessionRequest, db: Session = Depends(get_db)):
    db_session = repository.create_session(db=db, session=session)
    return service.create_session_service(db_session)

@app.get("/read-sessions/", response_model= Sessions)
def read_sessions_controller(db: Session = Depends(get_db)):
    db_session = repository.get_sessions(db)
    return service.read_session_service(db_session)

@app.get("/read-session-by-id/{session_id}", response_model=ResponseUnionSession)
def read_session_by_id_controller(session_id: str, db: Session = Depends(get_db)):
    db_session = repository.get_session_by_id(db, session_id=session_id)
    return service.read_session_by_id_service(db_session)

@app.get("/read-session-by-user-id/{user_id}", response_model=ResponseUnionSessions)
def read_session_by_user_id_controller(user_id: str, db: Session = Depends(get_db)):
    db_sessions = repository.get_session_by_user_id(db, user_id=user_id)
    db_user_ver = repository.get_user_ver_by_id(db, user_id=user_id)
    
    # Convert database rows to dictionaries
    sessions = [session._asdict() for session in db_sessions]
    user_ver = db_user_ver._asdict()

    # Create Pydantic model instance
    body = UserSessions(sessions=sessions, user=user_ver)
    return service.read_session_by_user_id_service(body)

@app.post("/update-session/{session_id}", response_model=ResponseUnionSession)
def update_user_controller(session_id: str, session: SessionUpdateRequest , db: Session = Depends(get_db)):
    db_session = repository.update_session(db, session_id=session_id, session=session)
    return service.update_session_service(db_session)

@app.post("/delete-session/{session_id}", response_model=ResponseUnionSession)
def delete_user_controller(session_id: str, db: Session = Depends(get_db)):
    db_user = repository.get_session_by_id(db, session_id=session_id)
    return service.delete_session_service(db_user)

@app.post("/create-user-ver/", response_model=ResponseUnionVerification)
def create_user_ver_controller(user_ver:Verification, db: Session = Depends(get_db)):
    db_session = repository.create_user_ver(db=db, user_ver=user_ver)
    return service.create_user_ver_service(db_session)

@app.get("/read-user-by-id/{user_id}", response_model=ResponseUnionVerification)
def read_user_by_id_controller(user_id: str, db: Session = Depends(get_db)):
    db_session = repository.get_user_ver_by_id(db, user_id=user_id)
    return service.read_user_ver_by_id_service(db_session)

@app.post("/update-user-ver/{user_id}", response_model=ResponseUnionVerification)
def update_user_controller(user_id: str, user_ver: VerificationUpdateRequest , db: Session = Depends(get_db)):
    db_session = repository.update_user_ver(db, user_id=user_id, user_ver=user_ver)
    return service.update_user_ver_service(db_session)

@app.post("/bulk-create-session/", response_model=ResponseUnionSessions)
def bulk_create_session_controller(sessions: List[SessionRequest], db: Session = Depends(get_db)):
    return service.bulk_create_session_service(sessions,db)

@app.get("/check-verification-status/{user_id}", response_model=ResponseUnionVerification)
def read_user_by_id_controller(user_id: str, db: Session = Depends(get_db)):
    db_session = repository.get_user_ver_by_id(db, user_id=user_id)
    return service.read_user_ver_by_id_service(db_session)

#@app.post("/check-verification/", response_model=ResponseUnionVerification)
#def check_verification_controller(sessions: List[SessionRequest], db: Session = Depends(get_db)):
#    return service.check_verification_service(sessions, db)
