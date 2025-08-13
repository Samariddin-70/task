from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.http import HttpResponse
from .models.cart import Card
from .utils import card_mask, phone_mask
import pandas as pd
import csv


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'masked_card_number',
        'formatted_phone',
        'status',
        'formatted_balance',
        'expire',
        'created_at'
    ]

    list_filter = [
        'status',
        'expire',
        ('phone', admin.EmptyFieldListFilter),
        'created_at',
    ]

    search_fields = [
        'card_number',
        'phone',
    ]

    readonly_fields = [
        'masked_card_number',
        'formatted_phone',
        'formatted_balance',
        'created_at',
        'updated_at'
    ]

    fieldsets = (
        ('Card Information', {
            'fields': ('card_number', 'masked_card_number', 'expire', 'status')
        }),
        ('Contact Information', {
            'fields': ('phone', 'formatted_phone')
        }),
        ('Financial Information', {
            'fields': ('balance', 'formatted_balance')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['export_selected_cards', 'activate_cards', 'deactivate_cards']

    def masked_card_number(self, obj):
        """Display masked card number in list view."""
        return card_mask(obj.card_number)
    masked_card_number.short_description = 'Card Number'

    def formatted_phone(self, obj):
        """Display formatted phone in list view."""
        if obj.phone:
            return phone_mask(obj.phone)
        return "-"
    formatted_phone.short_description = 'Phone'

    def formatted_balance(self, obj):
        """Display formatted balance in list view."""
        return f"{obj.balance:,.2f} UZS"
    formatted_balance.short_description = 'Balance'

    def export_selected_cards(self, request, queryset):
        """Export selected cards to CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cards_export.csv"'

        writer = csv.writer(response)
        writer.writerow(['Card Number', 'Expire', 'Phone', 'Status', 'Balance'])

        for card in queryset:
            writer.writerow([
                card.card_number,
                card.expire.strftime('%Y-%m-%d') if card.expire else '',
                card.phone or '',
                card.status,
                str(card.balance)
            ])

        self.message_user(request, f"Exported {queryset.count()} cards successfully.")
        return response
    export_selected_cards.short_description = "Export selected cards to CSV"

    def activate_cards(self, request, queryset):
        """Activate selected cards."""
        updated = queryset.update(status='active')
        self.message_user(request, f"Activated {updated} cards successfully.")
    activate_cards.short_description = "Activate selected cards"

    def deactivate_cards(self, request, queryset):
        """Deactivate selected cards."""
        updated = queryset.update(status='inactive')
        self.message_user(request, f"Deactivated {updated} cards successfully.")
    deactivate_cards.short_description = "Deactivate selected cards"

    def get_urls(self):
        """Add custom URLs for import functionality."""
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), name='cards_card_import'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """Add import button to changelist view."""
        extra_context = extra_context or {}
        extra_context['import_url'] = 'import-excel/'
        return super().changelist_view(request, extra_context)

    def import_excel_view(self, request):
        """Handle Excel file import."""
        if request.method == 'POST':
            excel_file = request.FILES.get('excel_file')

            if not excel_file:
                messages.error(request, 'Please select an Excel file.')
                return redirect('..')

            try:
                # Read Excel file
                df = pd.read_excel(excel_file)

                success_count = 0
                error_count = 0
                errors = []

                for index, row in df.iterrows():
                    try:
                        # Parse and validate data
                        card_data = self._parse_excel_row(row)

                        # Create or update card
                        card, created = Card.objects.get_or_create(
                            card_number=card_data['card_number'],
                            defaults=card_data
                        )

                        if not created:
                            # Update existing card
                            for key, value in card_data.items():
                                setattr(card, key, value)
                            card.save()

                        success_count += 1

                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {index + 2}: {str(e)}")

                # Show results
                if success_count > 0:
                    messages.success(request, f"Successfully imported {success_count} cards.")

                if error_count > 0:
                    error_msg = f"Failed to import {error_count} cards:\n" + "\n".join(errors[:10])
                    if len(errors) > 10:
                        error_msg += f"\n... and {len(errors) - 10} more errors."
                    messages.error(request, error_msg)

                return redirect('..')

            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                return redirect('..')

        # Render import form
        return render(request, 'admin/cards/card/import_excel.html')

    def _parse_excel_row(self, row):
        """Parse a single Excel row and return card data."""
        from .utils import parse_expire_date, validate_card_number, validate_phone_number

        # Extract data from row
        print("\n\n", row, "\n\n")
        card_number = str(row.get('card_number', '')).strip()
        expire_str = str(row.get('expire', '')).strip()
        phone = str(row.get('phone', '')).strip()
        status = str(row.get('status', 'active')).strip().lower()
        balance = float(row.get('balance', 0))

        # Validate card number
        is_valid, error_msg = validate_card_number(card_number)
        print(">>>>>>", is_valid, error_msg)
        if not is_valid:
            raise ValueError(f"Invalid card number: {error_msg}")

        # Validate phone number
        is_valid, error_msg = validate_phone_number(phone)
        if not is_valid:
            raise ValueError(f"Invalid phone number: {error_msg}")

        # Parse expire date
        expire_date = None
        if expire_str and expire_str != 'nan':
            expire_date = parse_expire_date(expire_str)
            if not expire_date:
                raise ValueError(f"Invalid expire date format: {expire_str}")

        # Validate status
        valid_statuses = ['active', 'inactive', 'expired']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of {valid_statuses}")

        # Validate balance
        if balance < 0 or balance > 1200000000:
            raise ValueError(f"Invalid balance: {balance}. Must be between 0 and 1,200,000,000")

        return {
            'card_number': card_number,
            'expire': expire_date,
            'phone': phone if phone and phone != 'nan' else None,
            'status': status,
            'balance': balance
        }


# Customize admin site
admin.site.site_header = "Card Management System"
admin.site.site_title = "Card Management"
admin.site.index_title = "Welcome to Card Management System"
