import io
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


def generate_excel_report(data: Dict[str, Any]) -> bytes:
    """
    Generate a multi-sheet Excel report with analytics data.
    
    Args:
        data: Dictionary containing 'employee_roi', 'project_profit', 'department_summary', 'overall'
    
    Returns:
        bytes: Excel file content
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Employee ROI sheet
        if 'employee_roi' in data and data['employee_roi']:
            df_roi = pd.DataFrame(data['employee_roi'])
            df_roi.to_excel(writer, sheet_name='Employee ROI', index=False)
        
        # Project Profit sheet
        if 'project_profit' in data and data['project_profit']:
            df_profit = pd.DataFrame(data['project_profit'])
            df_profit.to_excel(writer, sheet_name='Project Profit', index=False)
        
        # Department Summary sheet
        if 'department_summary' in data and data['department_summary']:
            df_dept = pd.DataFrame(data['department_summary'])
            df_dept.to_excel(writer, sheet_name='Department Summary', index=False)
        
        # Overall Summary sheet
        if 'overall' in data:
            overall_data = data['overall']
            df_overall = pd.DataFrame([overall_data])
            df_overall.to_excel(writer, sheet_name='Overall Summary', index=False)
    
    output.seek(0)
    return output.getvalue()


def generate_pdf_report(data: Dict[str, Any]) -> bytes:
    """
    Generate a PDF report with overall summary and top employees by ROI.
    
    Args:
        data: Dictionary containing 'employee_roi', 'project_profit', 'department_summary', 'overall'
    
    Returns:
        bytes: PDF file content
    """
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Employee Productivity & Cost Dashboard Report", title_style))
    story.append(Spacer(1, 20))
    
    # Generation timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"Generated on: {timestamp}", styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Overall Summary
    if 'overall' in data:
        story.append(Paragraph("Overall Summary", heading_style))
        overall = data['overall']
        
        overall_data = [
            ['Metric', 'Value'],
            ['Total Cost', f"${overall.get('total_cost', 0):,.2f}"],
            ['Total Revenue', f"${overall.get('total_revenue', 0):,.2f}"],
            ['ROI', f"{overall.get('roi', 0):.2%}" if overall.get('roi') else 'N/A']
        ]
        
        overall_table = Table(overall_data)
        overall_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(overall_table)
        story.append(Spacer(1, 30))
    
    # Top Employees by ROI
    if 'employee_roi' in data and data['employee_roi']:
        story.append(Paragraph("Top Employees by ROI", heading_style))
        
        # Sort employees by ROI (descending) and take top 5
        employees = sorted(data['employee_roi'], 
                         key=lambda x: x.get('roi', 0) if x.get('roi') else 0, 
                         reverse=True)[:5]
        
        if employees:
            employee_data = [['Employee', 'Department', 'ROI', 'Total Cost', 'Total Revenue']]
            for emp in employees:
                roi_str = f"{emp.get('roi', 0):.2%}" if emp.get('roi') else 'N/A'
                employee_data.append([
                    emp.get('employee_name', 'N/A'),
                    emp.get('department', 'N/A'),
                    roi_str,
                    f"${emp.get('total_cost', 0):,.2f}",
                    f"${emp.get('total_revenue', 0):,.2f}"
                ])
            
            employee_table = Table(employee_data)
            employee_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9)
            ]))
            
            story.append(employee_table)
    
    # Build PDF
    doc.build(story)
    output.seek(0)
    return output.getvalue()