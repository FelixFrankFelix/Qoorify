from utility.exceptions import ResponseConstant
import repository
from typing import List
from sqlalchemy.orm import Session
from schemas import SessionRequest, Verification, VerificationUpdateRequest, UserSessions
import repository

def create_session_service(body):
    if not body:
        return {
        "responseCode": ResponseConstant.DUPLICATE_RECORD.responseCode,
        "responseMessage": "email already exist", 
        }
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }

def read_session_service(body):
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }

def read_session_by_id_service(body):
    if body is None:
        return ResponseConstant.NO_SUCH_ISSUER
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }


def read_session_by_user_id_service(body):
    if not body:
        return ResponseConstant.NO_SUCH_ISSUER
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }
        

def update_session_service(body):
    if body is None:
        return ResponseConstant.NO_SUCH_ISSUER
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }


def delete_session_service(body):
    if body is None:
        return ResponseConstant.NO_SUCH_ISSUER
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }

def create_user_ver_service(body):
    if not body:
        return {
        "responseCode": ResponseConstant.DUPLICATE_RECORD.responseCode,
        "responseMessage": "email already exist", 
        }
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }

def read_user_ver_by_id_service(body):
    if body is None:
        return ResponseConstant.NO_SUCH_ISSUER
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }


def update_user_ver_service(body):
    if body is None:
        return ResponseConstant.NO_SUCH_ISSUER
    return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }


def bulk_create_session_service(db_sessions,db):
    #print(db_sessions)
    count = 0
    for session in db_sessions:
        repository.create_session(db=db,session=session)
        if session.sessionUserIsPresent == "YES":
            count += 1
    
    user_id = db_sessions[0].sessionUserId
    user_ver = repository.get_user_ver_by_id(db=db,user_id=user_id)
    new_user_ver = {}

    # Convert database rows to dictionaries
    sessions = [session.dict() for session in db_sessions]
    user_ver = user_ver._asdict() if user_ver is not None else None
    print(sessions,user_ver)
    
    # Create Pydantic model instance
    if not user_ver:
        new_user_ver = Verification(
            userId=user_id,
            userVerificationCount=count,
            userIsVerified="NO"
        )
        repository.create_user_ver(db=db, user_ver= new_user_ver)

        body = UserSessions(sessions=sessions, user=new_user_ver)

        return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }
        
    else: 
        user_ver_dict = user_ver
        user_ver_dict["userVerificationCount"] += count
        if user_ver_dict["userVerificationCount"] > 8:
            user_ver_dict["userIsVerified"] = "YES"

        update_data = VerificationUpdateRequest(
            userVerificationCount = user_ver_dict["userVerificationCount"],
            userIsVerified = user_ver_dict["userIsVerified"]
        )
        repository.update_user_ver(db=db,user_id=user_id,user_ver=update_data)

        user_ver ={
            "userId": user_id,
            "userVerificationCount": user_ver_dict["userVerificationCount"],
            "userIsVerified": user_ver_dict["userIsVerified"]
        }
        body = UserSessions(sessions=sessions, user=user_ver)

        return {
        "responseCode": ResponseConstant.SUCCESS.responseCode,
        "responseMessage": ResponseConstant.SUCCESS.responseMessage, 
        "body" : body
        }

   

    
        
    
    
       
