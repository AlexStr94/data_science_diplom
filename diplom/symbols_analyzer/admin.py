from django.contrib import admin

from .models import CellImage, Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    pass

admin.register(CellImage)
class CellImageAdmin(admin.ModelAdmin):
    fields = ('image', 'symbol')