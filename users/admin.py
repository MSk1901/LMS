from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение пользователей в админке"""
    list_display = ('email', 'is_superuser')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Отображение оплат в админке"""
    list_display = ('date', 'amount')
