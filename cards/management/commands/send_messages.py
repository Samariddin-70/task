from django.core.management.base import BaseCommand
from ...models.cart import Card
from ...utils import prepare_message, send_message
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Filterlangan kartalarga xabar yuborish'

    def add_arguments(self, parser):
        parser.add_argument(
            '--status',
            type=str,
            default='active',
            help='Status bo\'yicha filter (default: active)'
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
            '--lang',
            type=str,
            default='UZ',
            choices=['UZ', 'EN'],
            help='Xabar tili (default: UZ)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Haqiqiy xabar yubormasdan faqat ko\'rsatish'
        )

    def handle(self, *args, **options):
        # Filterlarni qo'llash
        queryset = Card.objects.all()

        if options['status']:
            queryset = queryset.filter(status=options['status'])
            self.stdout.write(f"Status filter: {options['status']}")

        if options['card_number']:
            queryset = queryset.filter(card_number__icontains=options['card_number'])
            self.stdout.write(f"Karta raqami filter: {options['card_number']}")

        if options['phone']:
            queryset = queryset.filter(phone__icontains=options['phone'])
            self.stdout.write(f"Telefon filter: {options['phone']}")

        cards = queryset.filter(phone__isnull=False).exclude(phone='')
        total_cards = cards.count()

        if total_cards == 0:
            self.stdout.write(
                self.style.WARNING('Telefon raqami bo\'lgan kartalar topilmadi!')
            )
            return

        self.stdout.write(f"Jami {total_cards} ta kartaga xabar yuboriladi")

        if options['dry_run']:
            self.stdout.write(self.style.WARNING("DRY RUN rejimi - haqiqiy xabar yuborilmaydi"))

        # Xabarlarni yuborish
        success_count = 0
        error_count = 0

        for card in cards:
            try:
                # Xabar tayyorlash
                message = prepare_message(
                    card.card_number,
                    float(card.balance),
                    options['lang']
                )

                if options['dry_run']:
                    self.stdout.write(f"📱 {card.get_formatted_phone()}: {message}")
                    success_count += 1
                else:
                    # Haqiqiy xabar yuborish (simulyatsiya)
                    if send_message(message, chat_id=12345):
                        success_count += 1
                        logger.info(f"Message sent to {card.phone}: {message}")
                    else:
                        error_count += 1
                        logger.error(f"Failed to send message to {card.phone}")

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"Xatolik {card.get_formatted_phone()}: {str(e)}")
                )

        # Natijalarni ko'rsatish
        if success_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Muvaffaqiyatli yuborildi: {success_count} ta xabar')
            )

        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(f'Xatolik: {error_count} ta xabar yuborilmadi')
            )
