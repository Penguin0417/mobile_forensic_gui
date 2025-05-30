# utils/data_exporter.py
import pandas as pd
from fpdf import FPDF

def export_data(table, format):
    rows = table.rowCount()
    data = []
    for row in range(rows):
        time = table.item(row, 0).text()
        content = table.item(row, 1).text()
        source = table.item(row, 2).text()
        data.append([time, content, source])

    df = pd.DataFrame(data, columns=["Time", "Content", "Source"])

    if format == "csv":
        df.to_csv("exported_data.csv", index=False)
    elif format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for _, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Time']} - {row['Content']} ({row['Source']})", ln=True)
        pdf.output("exported_data.pdf")
