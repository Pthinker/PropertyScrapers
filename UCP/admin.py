from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

import models


class PriceRangeListFilter(admin.SimpleListFilter):
    title = _('Price Range')
    parameter_name = 'cash_reported'

    def lookups(self, request, model_admin):
        return (
            ('10000', _('Under $10,000')),
            ('10000_25000', _('$10,000 - $25,000')),
            ('25000_50000', _('$25,000 - $50,000')),
            ('50000_100000', _('$50,000 - $100,000')),
            ('100000', _('Over $100,000')),
        )

    def queryset(self, request, queryset):
        if self.value() == '10000':
            return queryset.filter(cash_reported__lt=10000)
        elif self.value() == '10000_25000':
            return queryset.filter(cash_reported__gte=10000, cash_reported__lt=25000)
        elif self.value() == '25000_50000':
            return queryset.filter(cash_reported__gte=25000, cash_reported__lt=50000)
        elif self.value() == '50000_100000':
            return queryset.filter(cash_reported__gte=50000, cash_reported__lt=100000)
        elif self.value() == '100000':
            return queryset.filter(cash_reported__gte=100000)


class UnclaimedPropertyAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'date_added_to_site', 'source', 'owners_name', 'owners_address', 'type_of_property',
                    'cash_reported', 'reported_by', 'show_external_link']
    list_filter = [PriceRangeListFilter, 'type_of_property', 'reported_by']
    search_fields = ['property_id', 'owners_name', 'owners_address', 'type_of_property', 'reported_by']

admin.site.register(models.UnclaimedProperty, UnclaimedPropertyAdmin)


class NTypeUnclaimedPropertyAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'notification_date', 'date_reported', 'date_last_contact', 'owners_name', 'owners_address',
                    'type_of_property', 'cash_reported', 'show_external_link']
    list_filter = ['type_of_property', 'cash_reported', 'notification_date']
    search_fields = ['property_id', 'owners_name', 'owners_address', 'business_contact_information', 'type_of_property']

admin.site.register(models.NTypeUnclaimedProperty, NTypeUnclaimedPropertyAdmin)
