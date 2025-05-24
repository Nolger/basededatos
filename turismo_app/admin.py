from django.contrib import admin
from .models import *

class PlanSiteDetailInline(admin.TabularInline):
    model = PlanSiteDetail
    extra = 1

class TourRequestInline(admin.TabularInline):
    model = TourRequest
    extra = 1

@admin.register(TourPlan)
class TourPlanAdmin(admin.ModelAdmin):
    inlines = [PlanSiteDetailInline]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [TourRequestInline]

admin.site.register(TouristSite)
admin.site.register(TourRequest)
admin.site.register(AttentionRecord)
