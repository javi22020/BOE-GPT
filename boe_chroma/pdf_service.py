import aiohttp
import asyncio
import json
import time, os

async def parse_pdf_stream(response):
    async def read_exactly(response, n):
        data = b''
        async for chunk in response.content.iter_chunked(n):
            data += chunk
            if len(data) >= n:
                return data[:n]
        if len(data) == 0:
            raise EOFError("Stream ended unexpectedly")
        return data  # Return partial data if stream ends

    try:
        while True:
            try:
                metadata_length_bytes = await read_exactly(response, 4)
                metadata_length = int.from_bytes(metadata_length_bytes, byteorder='big')
                
                metadata_or_eof = await read_exactly(response, metadata_length)
                
                if metadata_or_eof == b'EOF':
                    print("Reached end of stream")
                    break
                
                metadata = json.loads(metadata_or_eof)
                pdf_content = await read_exactly(response, metadata['size'])
                yield metadata['index'], pdf_content
            except EOFError as e:
                print(f"Stream ended: {e}")
                break
            except Exception as e:
                print(f"Error parsing stream: {e}")
                break
    except Exception as e:
        print(f"Unexpected error: {e}")

async def get_boe_pdfs(date, max_retries=3, retry_delay=5):
    url = f'http://127.0.0.1:8000/boe_pdfs/{date}'
    os.makedirs(f"pdfs/{date}", exist_ok=True)
    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        pdf_count = 0
                        async for index, pdf_content in parse_pdf_stream(response):
                            with open(f'pdfs/{date}/pdf_{index}.pdf', 'wb') as f:
                                f.write(pdf_content)
                            print(f"Saved pdf_{index}.pdf")
                            pdf_count += 1
                        print(f"Total PDFs saved: {pdf_count}")
                        return
                    else:
                        print(f"Error: {response.status} - {await response.text()}")
            except aiohttp.ClientError as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                else:
                    print("Max retries reached. Unable to download PDFs.")
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

if __name__ == '__main__':
    asyncio.run(get_boe_pdfs('20240814'))