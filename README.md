# Django Card Management System

A comprehensive Django application for managing bank cards with Excel import/export functionality and messaging capabilities.

## Features

- **Card Management**: Create, read, update, and delete card records
- **Admin Interface**: Customized Django admin with filters and search
- **Excel Import**: Import cards from Excel files with data validation
- **CSV Export**: Export filtered card data via management command
- **Messaging System**: Send notifications to card holders (simulated)
- **Data Formatting**: Automatic formatting and masking of sensitive data

## Installation

1. **Create virtual environment:**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

2. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run migrations:**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

4. **Create superuser:**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`

5. **Generate sample Excel file:**
   \`\`\`bash
   python scripts/create_sample_excel.py
   \`\`\`

6. **Run development server:**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

## Usage

### Admin Interface
- Access admin at: `http://localhost:8000/admin/`
- Import Excel files using the "Import Excel File" button
- Filter cards by status, expire date, phone, and balance
- Export selected cards to CSV

### Management Commands

**Export Cards:**
\`\`\`bash
# Export all cards
python manage.py export_cards

# Export with filters
python manage.py export_cards --status active --output active_cards.csv

# Export specific fields
python manage.py export_cards --fields card_number status balance
\`\`\`

**Send Messages:**
\`\`\`bash
# Send messages to active cards (dry run)
python manage.py send_messages --status active --dry-run

# Send actual messages
python manage.py send_messages --status active --lang UZ

# Send to cards with specific phone pattern
python manage.py send_messages --phone "973" --lang EN
\`\`\`

## Data Format

### Excel Import Format
| Column | Description | Example |
|--------|-------------|---------|
| card_number | Card number | 8600 1234 5678 9012 |
| expire | Expiration date | 12/24, 2024-12, 12.2024 |
| phone | Phone number | 99 973 03 03, 973-03-03 |
| status | Card status | active, inactive, expired |
| balance | Balance amount | 1000.50 |

### Utility Functions
- `card_mask()`: Mask card numbers for display
- `phone_mask()`: Mask phone numbers for privacy
- `format_card()`: Format card numbers consistently
- `format_phone()`: Format phone numbers consistently
- `prepare_message()`: Create notification messages
- `send_message()`: Send messages (simulated)

## Project Structure
\`\`\`
card_management/
├── cards/
│   ├── management/commands/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── utils.py
│   └── views.py
├── templates/admin/
├── scripts/
└── requirements.txt
\`\`\`

## GitHub Workflow

Follow the branching strategy:
1. Create task branch from `staging`
2. Implement features and commit changes
3. Create PR: `task_branch` → `staging`
4. After review, create PR: `staging` → `prod`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
