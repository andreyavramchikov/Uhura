from django.contrib import admin

from .forms import PublicationEntityForm
from .models import Publication, PublicationEntity, Discount


class PublicationEntityInline(admin.TabularInline):
    model = PublicationEntity
    form = PublicationEntityForm
    extra = 1


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    inlines = (PublicationEntityInline,)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass

