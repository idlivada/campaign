from django.contrib import admin
from campaign.core.models import Campaign

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'chamber')
    fields = ('title', 'chamber', 'description', 'full_description', 'script', 'tweet_text')
admin.site.register(Campaign, CampaignAdmin)
