from django.contrib import admin

from .models import LogFrame, Milestone, RiskRating

admin.site.register(LogFrame)
admin.site.register(Milestone)
admin.site.register(RiskRating)
