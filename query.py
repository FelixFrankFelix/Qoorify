CREATE_SESSION = """
    INSERT INTO sessions (
        sessionId, 
        sessionUserId, 
        sessionUserIsPresent, 
        sessionLatitude, 
        sessionLongitude, 
        sessionCreatedAt, 
        sessionUpdatedAt, 
        sessionStatus
    ) 
    VALUES (
        :sessionId, 
        :sessionUserId, 
        :sessionUserIsPresent, 
        :sessionLatitude, 
        :sessionLongitude, 
        :sessionCreatedAt, 
        :sessionUpdatedAt, 
        :sessionStatus
    )
"""

READ_BY_SESSION_ID = """
    SELECT * FROM sessions 
    WHERE sessionId = :sessionId 
    AND sessionStatus != 'DELETED'
"""

READ_ALL = """
    SELECT * FROM sessions 
    WHERE sessionStatus != 'DELETED'
"""

READ_SESSION_BY_USER_ID = """
    SELECT * FROM sessions 
    WHERE sessionUserId = :sessionUserId 
    AND sessionStatus != 'DELETED'
"""

DELETE_SESSION = """
    UPDATE sessions 
    SET sessionStatus = 'DELETED' 
    WHERE sessionId = :sessionId
"""

UPDATE_SESSION = """
    UPDATE sessions 
    SET 
        sessionUserId = :sessionUserId,
        sessionUserIsPresent = :sessionUserIsPresent, 
        sessionLatitude = :sessionLatitude, 
        sessionLongitude = :sessionLongitude, 
        sessionUpdatedAt = :sessionUpdatedAt,
        sessionStatus = :sessionStatus
    WHERE 
        sessionId = :sessionId 
"""

DELETE_SESSION = """
    UPDATE sessions 
    SET sessionStatus = 'DELETED', sessionUpdatedAt = :sessionUpdatedAt 
    WHERE sessionId = :sessionId
"""

CREATE_USER_VER = """
    INSERT INTO verification (
        userId, 
        userVerificationCount, 
        userIsVerified
    ) 
    VALUES (
        :userId, 
        :userVerificationCount, 
        :userIsVerified
    )
"""

READ_BY_USER_ID = """
    SELECT * FROM verification 
    WHERE userId = :userId 
"""

UPDATE_USER_VER = """
    UPDATE verification 
    SET 
        userVerificationCount = :userVerificationCount, 
        userIsVerified = :userIsVerified
    WHERE 
        userId = :userId
"""