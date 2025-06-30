from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Announcement:
    news_id: str
    date_time: str
    company: str
    headline: str
    attachment_url: Optional[str] = None
    order_value: Optional[str] = None
    exchange: str = "UNKNOWN"
    symbol: Optional[str] = None

    def __str__(self):
        output = (
            f"[{self.exchange} | {self.symbol or 'N/A'}]\n"
            f"DateTime: {self.date_time}\n"
            f"Company: {self.company}\n"
            f"Headline: {self.headline}\n"
        )
        if self.attachment_url:
            output += f"AttachmentURL: {self.attachment_url}\n"
        output += f"Order Value: {self.order_value or 'Not found.'}"
        return output.strip()

    def to_dict(self) -> dict:
        """
        Converts the Announcement instance to a dict suitable for JSON serialization.
        """
        return {
            "DateTime": self.date_time,
            "Company": self.company,
            "Headline": self.headline,
            "AttachmentURL": self.attachment_url,
            "OrderValue": self.order_value,
            "Exchange": self.exchange,
            "Symbol": self.symbol
        }
