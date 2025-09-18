from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Proses, Tool, UserProfile, RiwayatPerbaikan, SukuCadang, RiwayatStok

# Mendefinisikan tampilan inline untuk UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Mendefinisikan admin baru untuk User yang menyertakan Profile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Mendaftarkan ulang User dengan admin kustom kita
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Mendaftarkan model-model Anda yang lain
admin.site.register(Proses)
admin.site.register(Tool)
admin.site.register(RiwayatPerbaikan)
admin.site.register(SukuCadang)
admin.site.register(RiwayatStok)