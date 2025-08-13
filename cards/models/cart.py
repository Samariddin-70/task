from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from ..utils import format_card, format_phone, card_mask, phone_mask, validate_card_number


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

  def __str__(self):
    return f"{self.get_masked_card_number()} - {self.get_status_display()}"

  def get_masked_card_number(self):
    """Return masked card number for display."""
    return card_mask(self.card_number)

  def get_formatted_card_number(self):
    """Return formatted card number."""
    return format_card(self.card_number)

  def get_masked_phone(self):
    """Return masked phone number for display."""
    return phone_mask(self.phone) if self.phone else ""

  def get_formatted_phone(self):
    """Return formatted phone number."""
    return format_phone(self.phone) if self.phone else ""

  def get_formatted_balance(self):
    """Return formatted balance with currency."""
    return f"{self.balance:,.2f} UZS"

  def is_expired(self):
    """Check if card is expired based on expire date."""
    if not self.expire:
      return False
    return self.expire < datetime.now()

  def save(self, *args, **kwargs):
    """Override save to format card number and phone before saving."""


    if self.card_number:
      self.card_number = format_card(self.card_number)
    if self.phone:
      self.phone = format_phone(self.phone)
    super().save(*args, **kwargs)
