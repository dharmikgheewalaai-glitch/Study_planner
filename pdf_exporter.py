import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def export_plan_to_pdf(df: pd.DataFrame, filename="study_plan.pdf"):
    """
    Exports DataFrame to a multi-page PDF with tables
    """
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("<b>Study Plan</b>", styles["Title"])
    elements.append(title)

    # Convert DataFrame to list of lists
    data = [df.columns.tolist()] + df.values.tolist()

    # Break into chunks (rows per page)
    chunk_size = 25
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]

        table = Table(chunk, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4CAF50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ]))
        elements.append(table)
        elements.append(PageBreak())

    doc.build(elements)
    return filename
