from django.contrib import admin

# Register your models here.
from .models import Publication, PublicationEntity, Discount


class PublicationEntityInline(admin.TabularInline):
    model = PublicationEntity
    extra = 1


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    inlines = (PublicationEntityInline,)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass
