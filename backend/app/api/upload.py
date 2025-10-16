from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.csv_loader import read_csv_file
from app.models.employee import Employee
from app.models.project import Project
from app.models.timesheet import Timesheet

router = APIRouter(prefix="/upload", tags=["Upload CSVs"])

@router.post("/{data_type}")
async def upload_csv(data_type: str, file: UploadFile, db: Session = Depends(get_db)):
    """
    Upload CSV data into employees, projects, or timesheets tables.
    """
    df = read_csv_file(file)
    inserted_rows = 0

    try:
        if data_type == "employees":
            for _, row in df.iterrows():
                employee = Employee(
                    id=int(row["id"]),
                    name=row["name"],
                    department=row["department"],
                    hourly_rate=float(row["hourly_rate"]),
                )
                db.merge(employee)  # merge avoids duplicate insert
            db.commit()
            inserted_rows = len(df)

        elif data_type == "projects":
            for _, row in df.iterrows():
                project = Project(
                    id=int(row["id"]),
                    name=row["name"],
                    revenue=float(row["revenue"]),
                )
                db.merge(project)
            db.commit()
            inserted_rows = len(df)

        elif data_type == "timesheets":
            for _, row in df.iterrows():
                timesheet = Timesheet(
                    id=int(row["id"]),
                    employee_id=int(row["employee_id"]),
                    project_id=int(row["project_id"]),
                    hours_worked=float(row["hours_worked"]),
                )
                db.merge(timesheet)
            db.commit()
            inserted_rows = len(df)

        else:
            raise HTTPException(status_code=400, detail="Invalid data_type parameter")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

    return {"status": "success", "rows_inserted": inserted_rows, "table": data_type}
