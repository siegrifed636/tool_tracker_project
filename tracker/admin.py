from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Proses, Tool, UserProfile, RiwayatPerbaikan, SukuCadang, RiwayatStok, ProductionLog, RiwayatGudang

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Proses)
admin.site.register(Tool)
admin.site.register(RiwayatPerbaikan)
admin.site.register(SukuCadang)
admin.site.register(RiwayatStok)
admin.site.register(ProductionLog)
admin.site.register(RiwayatGudang)