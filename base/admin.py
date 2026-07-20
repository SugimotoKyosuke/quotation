from django.contrib import admin
from base.models import Estimate, Project, CostEstimate, Service
from django.contrib.auth.models import Group

admin.site.register(Estimate)
admin.site.register(Project)
admin.site.register(CostEstimate)
admin.site.register(Service)
admin.site.unregister(Group)