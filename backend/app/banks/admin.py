from django.contrib import admin
from .models import Bank

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("id","name","bic","country","city","rating","is_active")
    search_fields = ("name","bic","country","city")
    list_filter = ("country","is_active")
