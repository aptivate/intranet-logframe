from django.contrib import admin

from .models import (LogFrame, Milestone, RiskRating, Output, Indicator,
                     SubIndicator)


class SubIndicatorInline(admin.TabularInline):
    model = SubIndicator
    extra = 1


class IndicatorAdmin(admin.ModelAdmin):
    inlines = (SubIndicatorInline,)

admin.site.register(LogFrame)
admin.site.register(Milestone)
admin.site.register(RiskRating)
admin.site.register(Output)
admin.site.register(Indicator, IndicatorAdmin)
