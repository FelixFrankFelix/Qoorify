from pydantic import BaseModel
from typing import Optional,Union,List
from datetime import datetime

class SessionRequest(BaseModel):
    sessionUserId: str
    sessionId: str
    sessionUserIsPresent: str
    sessionLatitude: float
    sessionLongitude: float
    sessionCreatedAt: datetime
    sessionUpdatedAt: datetime
    sessionStatus: str

class SessionResponse(BaseModel):
    sessionUserId: str
    sessionId: str
    sessionUserIsPresent: str
    sessionLatitude : float
    sessionLongitude: float
    sessionCreatedAt: datetime
    sessionUpdatedAt: datetime
    sessionStatus: str

class SessionUpdateRequest(BaseModel):
    sessionUserId: Optional[str] = None
    sessionUserIsPresent: Optional[str] = None
    sessionLatitude: Optional[float] = None
    sessionLongitude: Optional[float] = None
    sessionStatus: Optional[str] = None

class Verification(BaseModel):
    userId: str
    userVerificationCount: int
    userIsVerified: str

class VerificationUpdateRequest(BaseModel):
    userVerificationCount: Optional[int] = None
    userIsVerified: Optional[str] = None

class BaseResponse(BaseModel):
    responseCode: str
    responseMessage: str
    
class DetailedResponseSession(BaseModel):
    responseCode: str
    responseMessage: str
    body: SessionResponse

class DetailedResponseSessions(BaseModel):
    responseCode: str
    responseMessage: str
    body: List[SessionResponse]

class DetailedVerificationResponse(BaseModel):
    responseCode: str
    responseMessage: str
    body: Verification

class DetailedVerificationResponses(BaseModel):
    responseCode: str
    responseMessage: str
    body: List[Verification]

ResponseUnionSession = Union[DetailedResponseSession, BaseResponse]
ResponseUnionSessions = Union[DetailedResponseSessions, BaseResponse]
ResponseUnionVerifications = Union[DetailedVerificationResponses, BaseResponse]
ResponseUnionVerification = Union[DetailedVerificationResponse, BaseResponse]
