# main.py

import time
from datetime import datetime
from config import POLL_INTERVAL
from bse_client.watcher import fetch_announcements as fetch_bse_announcements
from nse_client.watcher import fetch_announcements as fetch_nse_announcements
from telegram.notifier import send_telegram_message

def normalize_key(value):
    return value.strip().lower() if value else ""

def main():
    seen_keys = set()
    last_date = None

    while True:
        try:
            today = datetime.today().date()

            # Reset cache on day change
            if today != last_date:
                seen_keys.clear()
                last_date = today
                print(f"[INFO] Resetting seen announcements for {today}")

            bse_anns = fetch_bse_announcements(from_date=today, to_date=today)
            nse_anns = fetch_nse_announcements(from_date=today, to_date=today)

            all_anns = bse_anns + nse_anns
            new_anns = []

            for ann in all_anns:
                # Create two deduplication keys
                symbol_key = (normalize_key(ann.symbol), normalize_key(ann.order_value))
                company_key = (normalize_key(ann.company), normalize_key(ann.order_value))

                if symbol_key in seen_keys or company_key in seen_keys:
                    continue

                # Add both keys to cache
                seen_keys.add(symbol_key)
                seen_keys.add(company_key)

                new_anns.append(ann)

            if new_anns:
                print(f"\n🔔 New Unique Announcements ({len(new_anns)}):\n")
                for announcement in new_anns:
                    send_telegram_message(announcement.__dict__)
                    print(announcement)
            else:
                print("[INFO] No new unique announcements.")

        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
