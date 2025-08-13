from django.core.management.base import BaseCommand
from django.db.models import Q
from ...models.cart import Card
import csv


class Command(BaseCommand):
    help = 'Kartalarni CSV formatida export qilish'

    def add_arguments(self, parser):
        parser.add_argument(
            '--status',
            type=str,
            help='Status bo\'yicha filter (active, inactive, expired)'
        )
        parser.add_argument(
            '--card-number',
            type=str,
            help='Karta raqami bo\'yicha filter'
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Telefon raqami bo\'yicha filter'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='cards_export.csv',
            help='Chiqish fayl nomi (default: cards_export.csv)'
        )
        parser.add_argument(
            '--fields',
            type=str,
            default='all',
            help='Export qilinadigan maydonlar (all, basic) yoki vergul bilan ajratilgan maydon nomlari'
        )

    def handle(self, *args, **options):
        # Filterlarni qo'llash
        queryset = Card.objects.all()

        if options['status']:
            queryset = queryset.filter(status=options['status'])
            self.stdout.write(f"Status filter qo'llandi: {options['status']}")

        if options['card_number']:
            queryset = queryset.filter(card_number__icontains=options['card_number'])
            self.stdout.write(f"Karta raqami filter qo'llandi: {options['card_number']}")

        if options['phone']:
            queryset = queryset.filter(phone__icontains=options['phone'])
            self.stdout.write(f"Telefon filter qo'llandi: {options['phone']}")

        # Maydonlarni aniqlash
        fields_option = options['fields']
        if fields_option == 'all':
            fields = ['card_number', 'expire', 'phone', 'status', 'balance', 'created_at', 'updated_at']
            headers = ['Karta Raqami', 'Amal Qilish Muddati', 'Telefon', 'Holat', 'Balans', 'Yaratilgan', 'Yangilangan']
        elif fields_option == 'basic':
            fields = ['card_number', 'status', 'balance']
            headers = ['Karta Raqami', 'Holat', 'Balans']
        else:
            fields = [f.strip() for f in fields_option.split(',')]
            headers = fields

        # CSV faylga yozish
        output_file = options['output']

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)

                # Sarlavhalarni yozish
                writer.writerow(headers)

                # Ma'lumotlarni yozish
                count = 0
                for card in queryset:
                    row = []
                    for field in fields:
                        if field == 'card_number':
                            row.append(card.get_formatted_card_number())
                        elif field == 'phone':
                            row.append(card.get_formatted_phone())
                        elif field == 'balance':
                            row.append(f"{card.balance:.2f}")
                        elif field == 'expire':
                            row.append(card.expire.strftime('%Y-%m-%d') if card.expire else '')
                        elif field == 'created_at':
                            row.append(card.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                        elif field == 'updated_at':
                            row.append(card.updated_at.strftime('%Y-%m-%d %H:%M:%S'))
                        else:
                            row.append(getattr(card, field, ''))

                    writer.writerow(row)
                    count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Muvaffaqiyatli export qilindi: {count} ta karta {output_file} faylga saqlandi'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Export qilishda xatolik: {str(e)}')
            )
