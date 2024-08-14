import requests as r
def get_boe_pdfs(date: str):
    """Get the BOE PDFs by date (aaaammdd)"""
    response = r.get(f"127.0.0.1:6550/boe_pdfs/{date}")
    if response.status_code != 200:
        return None
    else:
        for pdf in response.iter_content(chunk_size=1024):
            yield pdf