

from django.contrib import admin
from .models import Item, Category, ItemImage

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 10  

class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageInline]

admin.site.register(Item, ItemAdmin)
admin.site.register(Category)