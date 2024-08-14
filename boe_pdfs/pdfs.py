import requests as r
import os

def get_pdf_content_by_url(url: str):
    response = r.get(url)
    if response.status_code != 200:
        return None
    return response.content

class PDFSBOE:
    def __init__(self) -> None:
        self.session = r.Session()
        if not os.path.exists("pdfs"):
            os.makedirs("pdfs", exist_ok=True)

    async def get_boe_by_date(self, date: str):
        """Get the BOE by date (aaaammdd)"""
        url = f"https://boe.es/datosabiertos/api/boe/sumario/{date}"
        response = self.session.get(url=url, headers={"Accept": "application/json"})
        if response.status_code != 200:
            yield None
            return
        data = response.json()["data"]
        diarios = data["sumario"]["diario"]
        for diario in diarios:
            pdf_sumario = diario["sumario_diario"]["url_pdf"]["texto"]
            pdfs = [pdf_sumario]
            for seccion in diario["seccion"]:
                for departamento in seccion["departamento"]:
                    if departamento.__class__ == str:
                        continue
                    elif "epigrafe" in departamento.keys():
                        epigrafe = departamento["epigrafe"]
                        for epigrafe_item in epigrafe:
                            epigrafe_item = epigrafe_item["item"]
                            if isinstance(epigrafe_item, list):
                                for item in epigrafe_item:
                                    pdfs.append(item["url_pdf"]["texto"])
                            else:
                                pdfs.append(epigrafe_item["url_pdf"]["texto"])
                    elif "item" in departamento.keys():
                        item = departamento["item"]
                        if isinstance(item, list):
                            for item in item:
                                pdfs.append(item["url_pdf"]["texto"])
                        else:
                            pdfs.append(item["url_pdf"]["texto"])

        for pdf in pdfs:
            pdf_content = get_pdf_content_by_url(pdf)
            if pdf_content:
                yield pdf_content