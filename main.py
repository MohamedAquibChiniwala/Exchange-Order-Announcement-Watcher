# main.py

import time
from config import POLL_INTERVAL
from bse_client.watcher import fetch_announcements as fetch_bse_announcements
from nse_client.watcher import fetch_announcements as fetch_nse_announcements
from telegram.notifier import send_telegram_message

def main():
    while True:
        try:
            bse_anns = fetch_bse_announcements()
            nse_anns = fetch_nse_announcements()

            all_anns = bse_anns + nse_anns
            if all_anns:
                print(f"\n🔔 New Announcements ({len(all_anns)}):\n")
                for announcement in all_anns:
                    send_telegram_message(announcement.__dict__)
                    print(announcement)
            else:
                print("[INFO] No new announcements.")
        except Exception as e:
            print(f"[ERROR] {e}")
        
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
