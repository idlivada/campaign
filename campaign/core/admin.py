import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.contrib import admin
from campaign.core.models import Campaign, Member

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'chamber')
    fields = ('title', 'chamber', 'description', 'full_description', 'script', 'tweet_text', 'email')
admin.site.register(Campaign, CampaignAdmin)


def csv_export(modeladmin, request, queryset):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=members.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
            smart_str(u"ID"),
            smart_str(u"First Name"),
            smart_str(u"Last Name"),
            smart_str(u"Street"),
            smart_str(u"City"),
            smart_str(u"Zip"),
            smart_str(u"State"),
            smart_str(u"Email"),
            smart_str(u"Phone"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.firstname),
            smart_str(obj.lastname),
            smart_str(obj.street),
            smart_str(obj.city),
            smart_str(obj.zipcode),
            smart_str(obj.state),
            smart_str(obj.email),
            smart_str(obj.phone),
        ])
    return response
csv_export.short_description = u"Export CSV"

class MemberAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname')
    fields = ('firstname', 'lastname', 'street', 'city', 'state', 'zipcode', 'phone', 'email')
    actions = [csv_export]
admin.site.register(Member, MemberAdmin)
