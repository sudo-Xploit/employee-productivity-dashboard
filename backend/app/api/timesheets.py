from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.timesheet import Timesheet
from app.schemas.timesheet_schema import TimesheetCreate, TimesheetResponse

router = APIRouter(prefix="/timesheets", tags=["Timesheets"])

@router.post("/", response_model=TimesheetResponse)
def create_timesheet(entry: TimesheetCreate, db: Session = Depends(get_db)):
    db_entry = Timesheet(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/", response_model=list[TimesheetResponse])
def get_all_timesheets(db: Session = Depends(get_db)):
    return db.query(Timesheet).all()

@router.get("/{timesheet_id}", response_model=TimesheetResponse)
def get_timesheet(timesheet_id: int, db: Session = Depends(get_db)):
    ts = db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()
    if not ts:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    return ts

@router.put("/{timesheet_id}", response_model=TimesheetResponse)
def update_timesheet(timesheet_id: int, updated: TimesheetCreate, db: Session = Depends(get_db)):
    ts = db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()
    if not ts:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    for key, value in updated.dict().items():
        setattr(ts, key, value)
    db.commit()
    db.refresh(ts)
    return ts

@router.delete("/{timesheet_id}")
def delete_timesheet(timesheet_id: int, db: Session = Depends(get_db)):
    ts = db.query(Timesheet).filter(Timesheet.id == timesheet_id).first()
    if not ts:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    db.delete(ts)
    db.commit()
    return {"status": "deleted", "timesheet_id": timesheet_id}
