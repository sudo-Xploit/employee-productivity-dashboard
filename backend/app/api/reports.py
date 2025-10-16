from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.analytics import employee_roi, project_profit, department_summary, overall
from app.utils.report_generator import generate_excel_report, generate_pdf_report

router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/{report_type}")
def generate_report(report_type: str, db: Session = Depends(get_db)):
    """
    Generate and download analytics reports in Excel or PDF format.
    
    Args:
        report_type: Either 'excel' or 'pdf'
        db: Database session
    
    Returns:
        Response: File download with appropriate MIME type
    """
    if report_type not in ['excel', 'pdf']:
        raise HTTPException(
            status_code=400, 
            detail={"error": "Invalid report type. Use 'excel' or 'pdf'."}
        )
    
    try:
        # Gather all analytics data
        analytics_data = {
            'employee_roi': employee_roi(db),
            'project_profit': project_profit(db),
            'department_summary': department_summary(db),
            'overall': overall(db)
        }
        
        if report_type == 'excel':
            # Generate Excel report
            file_content = generate_excel_report(analytics_data)
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
        else:  # pdf
            # Generate PDF report
            file_content = generate_pdf_report(analytics_data)
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            media_type = "application/pdf"
        
        return Response(
            content=file_content,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": f"Failed to generate report: {str(e)}"}
        )