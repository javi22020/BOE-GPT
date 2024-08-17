import requests as r
import os

def get_pdf_content_by_url(url: str, session: r.Session):
    with session.get(url) as response:
        if response.status_code != 200:
            return None
        return response.content

class PDFSBOE:
    def __init__(self) -> None:
        if not os.path.exists("pdfs"):
            os.makedirs("pdfs", exist_ok=True)

    def get_boe_by_date(self, date: str):
        """Get the BOE by date (aaaammdd)"""
        url = f"https://boe.es/datosabiertos/api/boe/sumario/{date}"
        with r.Session() as session:
            with session.get(url, headers={"Accept": "application/json"}) as response:
                if response.status_code != 200:
                    yield None
                    return
                data = response.json()
            
            data = data["data"]
            diarios = data["sumario"]["diario"]
            for diario in diarios:
                pdf_sumario = diario["sumario_diario"]["url_pdf"]["texto"]
                pdfs = [pdf_sumario]
                for seccion in diario["seccion"]:
                    for departamento in seccion["departamento"]:
                        if isinstance(departamento, str):
                            continue
                        elif "epigrafe" in departamento:
                            epigrafe = departamento["epigrafe"]
                            for epigrafe_item in epigrafe:
                                epigrafe_item = epigrafe_item["item"]
                                if isinstance(epigrafe_item, list):
                                    for item in epigrafe_item:
                                        pdfs.append(item["url_pdf"]["texto"])
                                else:
                                    pdfs.append(epigrafe_item["url_pdf"]["texto"])
                        elif "item" in departamento:
                            item = departamento["item"]
                            if isinstance(item, list):
                                for item in item:
                                    pdfs.append(item["url_pdf"]["texto"])
                            else:
                                pdfs.append(item["url_pdf"]["texto"])
            
            try:
                for pdf in pdfs:
                    pdf_content = get_pdf_content_by_url(pdf, session)
                    if pdf_content:
                        yield pdf_content
            except Exception as e:
                print(f"Error downloading PDF: {e}")
                yield None
        return