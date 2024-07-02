from django.contrib import admin
from .models import CustomUser, Ads, LinuxDistribution, Banner, Profile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Ads)
admin.site.register(Banner)
admin.site.register(LinuxDistribution)
admin.site.register(Profile)
# admin.site.register(Comment)