from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def paginate_query(query, page, per_page):
  return query.limit(per_page).offset((page - 1) * per_page)

def getRecord(id: str, model: str, db: Session):
  recordDB = db.get(model, id)
  if recordDB is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Record not found!"
    )
  return recordDB