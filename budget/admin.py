# budget/admin.py

from django.contrib import admin
from .models import Expense, Income, Goal, UsedCredit, GlobalBudgetSetting

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('kid', 'title', 'amount', 'date')
    search_fields = ('kid', 'title')
    list_filter = ('date',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('kid', 'title', 'amount', 'date')
    search_fields = ('kid', 'title')
    list_filter = ('date',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('kid', 'title', 'amount', 'date')
    search_fields = ('kid',)
    list_filter = ('date',)


@admin.register(UsedCredit)
class UsedCreditAdmin(admin.ModelAdmin):
    list_display = ('kid', 'amount', 'date')
    search_fields = ('kid',)
    list_filter = ('date',)


@admin.register(GlobalBudgetSetting)
class GlobalBudgetSettingAdmin(admin.ModelAdmin):
    list_display = ('monthly_budget',)

    def has_add_permission(self, request):
        # Only one global budget record allowed
        return not GlobalBudgetSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
