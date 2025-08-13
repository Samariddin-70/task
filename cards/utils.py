import re
from datetime import datetime
from typing import Optional, Tuple

from django.core.exceptions import ValidationError


def card_mask(card_number: str) -> str:
    """
    Mask card number showing only first 4 and last 4 digits.
    Example: 8600123456789012 -> 8600 **** **** 9012
    """
    if not card_number:
        return ""

    # Remove all non-digit characters
    clean_number = re.sub(r'\D', '', str(card_number))

    if len(clean_number) < 8:
        return clean_number

    # Format as: first 4 + masked middle + last 4
    first_four = clean_number[:4]
    last_four = clean_number[-4:]
    middle_length = len(clean_number) - 8

    if middle_length > 0:
        masked_middle = '*' * min(middle_length, 8)  # Limit mask length
        return f"{first_four} {masked_middle[:4]} {masked_middle[4:]} {last_four}".strip()
    else:
        return f"{first_four} {last_four}"


def phone_mask(phone: str) -> str:
    """
    Mask phone number showing only first 2 and last 2 digits.
    Example: 99 973 03 03 -> 99 *** ** 03
    """
    if not phone:
        return ""

    # Remove all non-digit characters
    clean_phone = re.sub(r'\D', '', str(phone))

    if len(clean_phone) < 4:
        return clean_phone

    # Format as: first 2 + masked middle + last 2
    first_two = clean_phone[:2]
    last_two = clean_phone[-2:]
    middle_length = len(clean_phone) - 4

    if middle_length > 0:
        masked_middle = '*' * min(middle_length, 6)
        return f"{first_two} {masked_middle} {last_two}"
    else:
        return f"{first_two} {last_two}"


def format_card(raw_card: str) -> str:
    """
    Format card number to standard format: XXXX XXXX XXXX XXXX
    """
    if not raw_card:
        return ""

    # Remove all non-digit characters
    clean_card = re.sub(r'\D', '', str(raw_card))

    # Add spaces every 4 digits
    formatted = ' '.join([clean_card[i:i+4] for i in range(0, len(clean_card), 4)])
    return formatted


def format_phone(raw_phone: str) -> str:
    """
    Format phone number to standard format: XX XXX XX XX
    """
    if not raw_phone:
        return ""

    # Remove all non-digit characters
    clean_phone = re.sub(r'\D', '', str(raw_phone))

    if len(clean_phone) == 9:
        # Format as: XX XXX XX XX
        return f"{clean_phone[:2]} {clean_phone[2:5]} {clean_phone[5:7]} {clean_phone[7:9]}"
    elif len(clean_phone) == 12 and clean_phone.startswith('+998'):
        # Remove country code and format
        local_phone = clean_phone[3:]
        return f"{local_phone[:2]} {local_phone[2:5]} {local_phone[5:7]} {local_phone[7:9]}"

    return clean_phone


def parse_expire_date(expire_str: str) -> Optional[datetime]:
    """
    Parse various expire date formats and return datetime object.
    Supports: MM/YY, YYYY-MM, MM.YYYY, etc.
    """
    if not expire_str:
        return None

    expire_str = str(expire_str).strip()

    # Try different date formats
    formats = [
        '%m/%y',      # 12/24
        '%Y-%m',      # 2024-12
        '%m.%Y',      # 12.2024
        '%m/%Y',      # 12/2024
        '%Y/%m',      # 2024/12
        '%m-%Y',      # 12-2024
    ]

    for fmt in formats:
        try:
            parsed_date = datetime.strptime(expire_str, fmt)
            # If year is less than 2000, assume it's 20XX
            if parsed_date.year < 2000:
                parsed_date = parsed_date.replace(year=parsed_date.year + 2000)
            return parsed_date
        except ValueError:
            continue

    return None


def prepare_message(card_number: str, balance: float, lang: str = "UZ") -> str:
    """
    Prepare message template for card notifications.
    """
    masked_card = card_mask(card_number)
    formatted_balance = f"{balance:,.2f}"

    if lang.upper() == "UZ":
        return f"Sizning kartangiz {masked_card} aktiv va foydalanishga {formatted_balance} UZS mavjud!"
    elif lang.upper() == "EN":
        return f"Your card {masked_card} is active with {formatted_balance} UZS available!"
    else:
        return f"Sizning kartangiz {masked_card} aktiv va foydalanishga {formatted_balance} UZS mavjud!"


def send_message(message: str, chat_id: int = 12345) -> bool:
    """
    Simulate sending message via Telegram bot.
    In production, this would use actual Telegram API.
    """
    try:
        # Simulate message sending
        print(f" Sending to chat_id {chat_id}: {message}")

        # Here you would implement actual Telegram bot logic:
        # bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
        # bot.send_message(chat_id=chat_id, text=message)

        return True
    except Exception as e:
        print(f"Failed to send message: {e}")
        return False


def validate_card_number(card_number: str) -> Tuple[bool, str]:
    """
    Validate card number format and return (is_valid, error_message).
    """
    if not card_number:
        raise ValidationError("Card number must not be empty")

    clean_card = re.sub(r'\D', '', str(card_number))

    if len(clean_card) == 17:
        raise ValidationError("Card number length error")
    if not clean_card.startswith('8600'):
        return False, "Card number must start with 8600"

    return True, ""


def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number format and return (is_valid, error_message).
    """
    if not phone:
        return True, ""  # Phone is optional

    clean_phone = re.sub(r'\D', '', str(phone))

    if len(clean_phone) not in [9, 13]:
        return False, "Phone number must be 9 or 13 digits"

    if len(clean_phone) == 12 and not clean_phone.startswith('+998'):
        return False, "13-digit phone must start with +998"

    return True, ""
