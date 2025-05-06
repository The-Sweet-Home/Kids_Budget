from datetime import date
from django.db.models import Sum
from .models import Income, Expense, Goal, UsedCredit, GlobalBudgetSetting

def calculate_financials(kid_name):
    # Get current month and year
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Filter incomes and expenses for the current month
    monthly_incomes = Income.objects.filter(
        kid=kid_name,
        date__year=current_year,
        date__month=current_month
    )

    monthly_expenses = Expense.objects.filter(
        kid=kid_name,
        date__year=current_year,
        date__month=current_month
    )

    monthly_used_credit = UsedCredit.objects.filter(
        kid=kid_name,
        date__year=current_year,
        date__month=current_month
    )
    previous_monthly_used_credit = UsedCredit.objects.filter(
        kid=kid_name,
        date__year=current_year,
        date__month=current_month - 1
    )

    sum_monthly_income = monthly_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    sum_monthly_expense = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    total_income = Income.objects.filter(kid=kid_name).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Expense.objects.filter(kid=kid_name).aggregate(Sum('amount'))['amount__sum'] or 0
    total_goal = Goal.objects.filter(kid=kid_name).aggregate(Sum('amount'))['amount__sum'] or 0
    total_monthly_used_credit = monthly_used_credit.aggregate(Sum('amount'))['amount__sum'] or 0
    previous_total_monthly_used_credit = previous_monthly_used_credit.aggregate(Sum('amount'))['amount__sum'] or 0

    monthly_budget = GlobalBudgetSetting.objects.first().monthly_budget
    monthly_debit = GlobalBudgetSetting.objects.first().monthly_budget + total_monthly_used_credit
    goal_instance = Goal.objects.filter(kid=kid_name).first()
    goal = goal_instance.amount if goal_instance else 0

    monthly_credit = max(GlobalBudgetSetting.objects.first().monthly_budget - total_monthly_used_credit, 0)
    credit = max(GlobalBudgetSetting.objects.first().monthly_budget - total_monthly_used_credit - previous_total_monthly_used_credit, 0)
    overall_balance = total_income - total_expense
    overall_monthly_balance = sum_monthly_income - sum_monthly_expense
    debit = monthly_budget + overall_monthly_balance

    return {
        'date': today,
        'monthly_incomes': monthly_incomes,
        'monthly_expenses': monthly_expenses,
        'sum_monthly_income': sum_monthly_income,
        'sum_monthly_expense': sum_monthly_expense,
        'total_income': total_income,
        'total_expense': total_expense,
        'total_goal': total_goal,
        'goal': goal,
        'total_used_credit': total_monthly_used_credit,
        'monthly_budget': monthly_budget,
        'monthly_debit': monthly_debit,
        'credit': credit,
        'overall_balance': overall_balance,
        'debit': debit,
    }

