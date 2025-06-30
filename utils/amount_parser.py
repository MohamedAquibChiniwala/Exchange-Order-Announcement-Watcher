import re
from typing import Optional

def parse_amount_to_crores(amount, unit):
    amount = amount.replace(',', '').strip()
    try:
        value = float(amount)
    except:
        return None

    unit = unit.lower() if unit else ''
    if unit in ['lakh', 'lakhs']:
        return value / 100
    elif unit in ['million', 'mn']:
        return value * 0.1
    elif unit in ['billion']:
        return value * 100
    elif unit in ['crore', 'cr']:
        return value
    else:
        return value / 1e7

def extract_single_order_value(text) -> Optional[str]:
    pattern = r"(?:₹|Rs\.?|INR)\s*([\d,]+(?:\.\d+)?)\s*(crore|cr|lakh|lakhs|million|mn|billion)?"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    for amount, unit in matches:
        value_in_crore = parse_amount_to_crores(amount, unit)
        if value_in_crore and value_in_crore > 0.01:
            return f"₹{value_in_crore:.2f} crore"
    return None
