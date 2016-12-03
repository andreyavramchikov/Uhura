from django.contrib import admin

# Register your models here.
from .models import Product, ProductAudio, ProductPDF, ProductPaperback


class ProductAudioInline(admin.TabularInline):
    model = ProductAudio
    extra = 1


class ProductPDFInline(admin.TabularInline):
    model = ProductPDF
    extra = 1


class ProductPaperbackInline(admin.TabularInline):
    model = ProductPaperback
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (
        ProductAudioInline, ProductPDFInline, ProductPaperbackInline,
    )