# nse_client/watcher.py

from datetime import datetime
from nse import NSE
from models.announcement import Announcement
from utils.pdf_utils import download_pdf_like_browser, extract_pdf_text
from utils.amount_parser import extract_single_order_value

seen_nse_ids = set()

def fetch_announcements(from_date: datetime, to_date: datetime) -> list[Announcement]:
    new_announcements = []

    target_descs = {
        'Bagging/Receiving of orders/contracts',
        'Awarding of order(s)/contract(s)'
    }

    with NSE(download_folder="./nse_cache", server=False) as nse:
        announcements = nse.announcements(from_date=from_date, to_date=to_date)

    for item in announcements:
        if item.get("desc") not in target_descs:
            continue

        symbol = item.get("symbol", "UNKNOWN")
        raw_dt = item.get("an_dt", "")  # format: '30-Jun-2025 18:09:31'
        try:
            dt = datetime.strptime(raw_dt, "%d-%b-%Y %H:%M:%S")
            parsed_date_time = dt.strftime("%I:%M:%S %p %d-%m-%Y")
        except ValueError:
            parsed_date_time = raw_dt

        unique_id = f"{symbol}-{raw_dt}"
        if unique_id in seen_nse_ids:
            continue
        seen_nse_ids.add(unique_id)

        attachment_url = item.get("attchmntFile")
        order_value = None

        if attachment_url:
            pdf_path = download_pdf_like_browser(attachment_url)
            if pdf_path:
                text = extract_pdf_text(pdf_path)
                order_value = extract_single_order_value(text)

        announcement = Announcement(
            news_id=unique_id,
            date_time=parsed_date_time,
            company=item.get("sm_name", ""),
            headline=item.get("attchmntText", ""),
            attachment_url=attachment_url,
            order_value=order_value,
            exchange="NSE",
            symbol=item.get("symbol", "")
        )

        new_announcements.append(announcement)

    return new_announcements
