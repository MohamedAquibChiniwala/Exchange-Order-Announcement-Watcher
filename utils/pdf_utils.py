import os
import requests
import fitz  # PyMuPDF

def download_pdf_like_browser(url, save_dir="./pdfs"):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bseindia.com",
        "Accept": "application/pdf"
    }
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.basename(url)
    file_path = os.path.join(save_dir, filename)

    try:
        with requests.get(url, headers=headers, stream=True, timeout=10) as r:
            r.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return file_path
    except Exception as e:
        print(f"[!] Failed to download PDF: {e}")
        return None

def extract_pdf_text(file_path):
    try:
        with fitz.open(file_path) as doc:
            return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        print(f"[!] Failed to extract PDF text: {e}")
        return ""
