import pandas as pd
from datetime import datetime, timedelta
import random

# Sample ma'lumotlar
sample_data = [
    {
        'card_number': '8600 4835 2559 2899',
        'expire': '2025-07',
        'phone': '973-03-03',
        'status': 'expired',
        'balance': 200.00
    },
    {
        'card_number': '8600855254356990',
        'expire': '03.2026',
        'phone': '',
        'status': 'active',
        'balance': 842714800.00
    },
    {
        'card_number': '8600327218840361',
        'expire': '2026-08',
        'phone': '99 973 03 03',
        'status': 'active',
        'balance': 22300.00
    },
    {
        'card_number': '8600 3901 0981 2774',
        'expire': '04/25',
        'phone': '',
        'status': 'active',
        'balance': 8911200.00
    },
    {
        'card_number': '8600 0871 2045 1520',
        'expire': '11.2026',
        'phone': '973-03-03',
        'status': 'expired',
        'balance': 400.00
    },
    {
        'card_number': '8600910092834567',
        'expire': '07/26',
        'phone': '',
        'status': 'expired',
        'balance': 684214300.00
    },
    {
        'card_number': '8600 1234 5678 9012',
        'expire': '12/24',
        'phone': '99 973 03 03',
        'status': 'inactive',
        'balance': 5000.00
    },
    {
        'card_number': '8600 7843 9910 1122',
        'expire': '06.2024',
        'phone': '',
        'status': 'inactive',
        'balance': 0.00
    }
]

# DataFrame yaratish
df = pd.DataFrame(sample_data)

# Excel faylga saqlash
df.to_excel('sample_cards.xlsx', index=False)
print("Sample Excel fayl yaratildi: sample_cards.xlsx")
