import aiohttp
import os
import asyncio

async def get_pdf_content_by_url(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        if response.status != 200:
            return None
        return await response.read()

class PDFSBOE:
    def __init__(self) -> None:
        if not os.path.exists("pdfs"):
            os.makedirs("pdfs", exist_ok=True)

    async def get_boe_by_date(self, date: str):
        """Get the BOE by date (aaaammdd)"""
        url = f"https://boe.es/datosabiertos/api/boe/sumario/{date}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"Accept": "application/json"}) as response:
                if response.status != 200:
                    yield None
                    return
                data = await response.json()
            
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

            for pdf in pdfs:
                pdf_content = await get_pdf_content_by_url(pdf, session)
                if pdf_content:
                    yield pdf_content