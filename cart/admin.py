from django.contrib import admin

# Register your models here.

from .models import Order, Item

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'region', 'date')
    list_filter = ('region', 'date')
    search_fields = ('user__username',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'order', 'price', 'quantity')
    list_filter = ('movie',)
    search_fields = ('movie__name',)