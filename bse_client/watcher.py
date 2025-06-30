# bse_client/watcher.py

from bse import BSE
from datetime import datetime
from models.announcement import Announcement
from utils.pdf_utils import download_pdf_like_browser, extract_pdf_text
from utils.amount_parser import extract_single_order_value
from typing import Optional
seen_ids = set()

def extract_bse_symbol(nsurl: str) -> Optional[str]:
    try:
        return nsurl.strip("/").split("/")[-2]
    except Exception:
        return None

def fetch_announcements() -> list[Announcement]:
    today = datetime.today()
    new_announcements = []

    with BSE(download_folder="./") as bse:
        data = bse.announcements(
            page_no=1,
            from_date=today,
            to_date=today,
            category='Company Update',
            subcategory='Award of Order / Receipt of Order'
        )

        table_data = data.get("Table", [])
        new_items = [item for item in table_data if item.get("NEWSID") not in seen_ids]

        for item in table_data:
            seen_ids.add(item.get("NEWSID"))

        for item in new_items:
            attachment = item.get('ATTACHMENTNAME')
            attachment_url = f"https://www.bseindia.com/xml-data/corpfiling/AttachLive/{attachment}" if attachment else None
            order_value = None

            if attachment_url:
                pdf_path = download_pdf_like_browser(attachment_url)
                if pdf_path:
                    text = extract_pdf_text(pdf_path)
                    order_value = extract_single_order_value(text)

            raw_dt = item.get("DT_TM", "")
            try:
                dt = datetime.strptime(raw_dt, "%Y-%m-%dT%H:%M:%S.%f")
                parsed_date_time = dt.strftime("%I:%M:%S %p %d-%m-%Y")
            except ValueError:
                parsed_date_time = raw_dt

            nsurl = item.get("NSURL", "")
            symbol = extract_bse_symbol(nsurl)

            announcement = Announcement(
                news_id=item.get("NEWSID", ""),
                date_time=parsed_date_time,
                company=item.get("SLONGNAME", ""),
                headline=item.get("HEADLINE", ""),
                attachment_url=attachment_url,
                order_value=order_value,
                exchange="BSE",
                symbol=symbol.upper()
            )

            new_announcements.append(announcement)

    return new_announcements
