from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_forecast_pdf(location, forecast_df):
    file_name = f"forecast_{location}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    y = 800
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Forecast Report - {location}")

    y -= 40
    c.setFont("Helvetica", 10)

    for _, row in forecast_df.tail(10).iterrows():
        c.drawString(50, y, f"{row['ds'].date()} → {int(row['yhat'])} cases")
        y -= 15

    c.save()
    return file_name
