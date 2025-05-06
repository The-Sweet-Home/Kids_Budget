from django.db import models
from datetime import date
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


KID_CHOICES = [
        ('Shaina', 'shaina'),
        ('Viana', 'viana'),
    ]

class FinancialElement(models.Model):
    kid = models.CharField(max_length=10, choices=KID_CHOICES)
    title = models.CharField(max_length=100, default="None")
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True


class Expense(FinancialElement):
    def __str__(self):
        return f"[Expense] {self.kid} - {self.title} - ${self.amount} ({self.date})"


class Income(FinancialElement):
    def __str__(self):
        return f"[Income] {self.kid} - {self.title} - ${self.amount} ({self.date})"


class Goal(FinancialElement):
    def __str__(self):
        return f"[Goal] {self.kid} - {self.title} - ${self.amount} ({self.date})"


class UsedCredit(FinancialElement):
    def clean(self):
        from .utils import calculate_financials
        data = calculate_financials(self.kid)
        credit_available = data['credit']

        if self.amount > credit_available:
            raise ValidationError(
                f"Used credit (${self.amount}) exceeds available credit (${credit_available:.2f}) for {self.kid}."
            )

    def __str__(self):
        return f"[Credit] {self.kid} - ${self.amount} on {self.date}"



class GlobalBudgetSetting(models.Model):
    monthly_budget = models.FloatField(default=25.0)

    def __str__(self):
        return f"Global Monthly Budget: ${self.monthly_budget}"

    class Meta:
        verbose_name = "Global Budget Setting"
        verbose_name_plural = "Global Budget Setting"
