from django.contrib import admin

from dispatches.models import Dispatch, Unit,Follower


class DispatchAdmin(admin.ModelAdmin):
    pass

admin.site.register(Follower)
admin.site.register(Unit)

admin.site.register(Dispatch, DispatchAdmin)
