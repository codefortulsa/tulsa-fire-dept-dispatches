from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from dispatches.models import (
    Dispatch, Follower, Profile, RawDispatch, Station, Unit, UnitFollower)

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile


class UserProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.register(Dispatch)
admin.site.register(Follower)
admin.site.register(RawDispatch)
admin.site.register(Station)
admin.site.register(Unit)
admin.site.register(UnitFollower)
admin.site.register(User, UserProfileAdmin)
