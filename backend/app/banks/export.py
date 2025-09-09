from io import BytesIO
from openpyxl import Workbook
from datetime import datetime

def export_banks_xlsx(qs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Banks"
    ws.append(["ID","Name","BIC","Country","City","Rating","Active","SWIFT","License","Site"])
    for b in qs:
        ws.append([b.id,b.name,b.bic,b.country,b.city,b.rating,b.is_active,b.swift,b.license_number,b.site])
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    filename = f"banks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return stream.getvalue(), filename
