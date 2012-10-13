from django.contrib import admin

from dispatches.models import Dispatch


class DispatchAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dispatch, DispatchAdmin)
