from django.db import models
from django.utils import timezone


class UnclaimedProperty(models.Model):
    property_id = models.BigIntegerField(unique=True, verbose_name='Property Id')
    date_added_to_site = models.CharField(max_length=20, verbose_name='Date')
    source = models.CharField(max_length=20, verbose_name='Source')
    owners_name = models.TextField(verbose_name='Owner(s) Name')
    owners_address = models.TextField(verbose_name='Reported Owner Address')
    type_of_property = models.CharField(max_length=2000, verbose_name='Type of Property')
    cash_reported_text = models.CharField(max_length=100, verbose_name='Cash Reported (Text)')
    cash_reported = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cash Reported')
    reported_by = models.CharField(max_length=2000, verbose_name='Reported By')
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s - %s' % (self.property_id, self.owners_name)

    def show_external_link(self):
        return '<a href="https://ucpi.sco.ca.gov/ucp/PropertyDetails.aspx?propertyID=%s" target="_blank">%s</a>' % (self.property_id, self.property_id)
    show_external_link.allow_tags = True
    show_external_link.short_description = 'UCP Site Link'
    show_external_link.admin_order_field = 'property_id'

    class Meta:
        verbose_name = 'Unclaimed Property P Type'
        verbose_name_plural = "Unclaimed Properties P Type"


class NTypeUnclaimedProperty(models.Model):
    property_id = models.BigIntegerField(unique=True, verbose_name='Property Id')
    notification_date = models.CharField(max_length=20, verbose_name='Notification Date')
    date_reported = models.CharField(max_length=20, verbose_name='Date Reported')
    date_last_contact = models.CharField(max_length=20, verbose_name='Date of Last Contact')
    owners_name = models.TextField(verbose_name='Owner(s) Name')
    owners_address = models.TextField(verbose_name='Reported Owner Address')
    business_contact_information = models.TextField(verbose_name='Business Contact Information')
    type_of_property = models.CharField(max_length=2000, verbose_name='Type of Property')
    cash_reported = models.CharField(max_length=100, verbose_name='Cash Reported')
    shares_reported = models.CharField(max_length=100, verbose_name='Shares Reported')
    name_security_reported = models.CharField(max_length=500, verbose_name='Name of Security Reported')
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s - %s' % (self.property_id, self.owners_name)

    def show_external_link(self):
        return '<a href="https://ucpi.sco.ca.gov/ucp/NoticeDetails.aspx?propertyRecID=%s" target="_blank">%s</a>' % (self.property_id, self.property_id)
    show_external_link.allow_tags = True
    show_external_link.short_description = 'UCP Site Link'
    show_external_link.admin_order_field = 'property_id'

    class Meta:
        verbose_name = 'Unclaimed Property N Type'
        verbose_name_plural = "Unclaimed Properties N Type"