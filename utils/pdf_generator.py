# utils/pdf_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_judge_pdf(report_text: str) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x = 40
    y = height - 40
    max_width = width - 80
    line_height = 14

    # Split text into lines and wrap it manually
    from textwrap import wrap
    lines = []
    for paragraph in report_text.split("\n"):
        wrapped = wrap(paragraph, width=100)
        lines.extend(wrapped if wrapped else [""])

    for line in lines:
        if y <= 40:
            c.showPage()
            y = height - 40
        c.drawString(x, y, line)
        y -= line_height

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
