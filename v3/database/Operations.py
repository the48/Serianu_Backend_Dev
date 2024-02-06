from sqlalchemy.orm import Session

from . import Models, Schemas

def get_requestID(db: Session, requestID: str):
    return db.query(Models.Request).filter(Models.Request.RequestID == requestID).first()


def create_requestID(db: Session, request: Schemas.RequestCreate):
    request = Models.Request(RequestID = request.RequestID, Payload = request.Payload, Timestamp = request.Timestamp)

    db.add(request)
    db.commit()
    db.refresh(request)
    return request