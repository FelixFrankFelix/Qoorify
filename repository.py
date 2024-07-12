from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
#from model.request.UserRequest import UserCreate, UserUpdate
from typing import List
from fastapi import HTTPException
#from repository.database.query import UserQuery
import query
from schemas import SessionRequest,SessionUpdateRequest,Verification,VerificationUpdateRequest
import json


def get_session_by_id(db: Session, session_id: str):
    result = db.execute(text(query.READ_BY_SESSION_ID), 
                        {'sessionId': session_id})
    return result.fetchone()

def get_sessions(db: Session):
    result = db.execute(text(query.READ_ALL))
    return result.fetchall()

def create_session(db: Session, session: SessionRequest):
    session_created_at = datetime.now()
    session_updated_at = session_created_at
    db.execute(
        text(query.CREATE_SESSION),
        {
            'sessionId': session.sessionId,
            'sessionUserId': session.sessionUserId,
            'sessionUserIsPresent': session.sessionUserIsPresent,
            'sessionLatitude': session.sessionLatitude,
            'sessionLongitude': session.sessionLongitude,
            'sessionCreatedAt': session_created_at,
            'sessionUpdatedAt': session_updated_at,
            'sessionStatus': 'ACTIVE'
        }
    )
    db.commit()
    return get_session_by_id(db, session.sessionId)

def get_session_by_user_id(db: Session, user_id: str):
    result = db.execute(text(query.READ_SESSION_BY_USER_ID), 
                        {'sessionUserId': user_id})
    return result.fetchall()

def update_session(db: Session, session_id: str, session: SessionUpdateRequest):
    # Fetch the current user from the database
    db_session = get_session_by_id(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    # Define the update dictionary with values passed or default to existing values
    update_data = {
        'sessionUserId': session.sessionUserId if session.sessionUserId else db_session.sessionUserId,
        'sessionUserIsPresent': session.sessionUserIsPresent if session.sessionUserIsPresent else db_session.sessionUserIsPresent,
        'sessionLatitude': session.sessionLatitude if session.sessionLatitude else db_session.sessionLatitude,
        'sessionLongitude': session.sessionLongitude if session.sessionLongitude else db_session.sessionLongitude,
        'sessionUpdatedAt': datetime.now(),
        'sessionStatus': session.sessionStatus if session.sessionStatus else db_session.sessionStatus
    }

    update_data['sessionId'] = session_id
    db.execute(text(query.UPDATE_SESSION),update_data)
    db.commit()

    # Return the updated user
    return get_session_by_id(db, session_id)

def delete_session(db: Session, session_id: str):
    session_updated_at = datetime.now()
    db.execute(
        text(query.DELETE_SESSION),
        {'session_updated_at': session_updated_at, 'session_id': session_id}
    )
    db.commit()
    return get_session_by_id(db, session_id)

def create_user_ver(db: Session, user_ver: Verification):
    db.execute(
        text(query.CREATE_USER_VER),
        {
            'userId': user_ver.userId,
            'userVerificationCount': user_ver.userVerificationCount,
            'userIsVerified': user_ver.userIsVerified,
        }
    )
    db.commit()
    return get_user_ver_by_id(db, user_ver.userId)

def get_user_ver_by_id(db: Session, user_id: str):
    result = db.execute(text(query.READ_BY_USER_ID), 
                        {'userId': user_id})
    return result.fetchone()

def update_user_ver(db: Session, user_id: str, user_ver: VerificationUpdateRequest):
    # Fetch the current user from the database
    db_session = get_user_ver_by_id(db, user_id=user_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Define the update dictionary with values passed or default to existing values
    update_data = {
        'userVerificationCount': user_ver.userVerificationCount if user_ver.userVerificationCount else db_session.userVerificationCount,
        'userIsVerified': user_ver.userIsVerified if user_ver.userIsVerified else db_session.userIsVerified
    }

    update_data['userId'] = user_id
    db.execute(text(query.UPDATE_USER_VER),update_data)
    db.commit()
    return get_user_ver_by_id(db, user_id)