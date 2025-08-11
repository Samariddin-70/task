from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Card(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]

    card_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="Card number (e.g., 8600 1234 5678 9012)"
    )
    expire = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Expiration date"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Phone number (e.g., 99 973 03 03)"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1200000000)  # 1.2 billion UZS
        ],
        default=0.00
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'




