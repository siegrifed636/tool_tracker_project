# tracker/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views # Impor view login/logout
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tracker/logout.html'), name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('', views.daftar_proses, name='daftar_proses'),
    path('proses/<int:proses_id>/', views.daftar_tool, name='daftar_tool'),
    path('tool/tambah/', views.tambah_tool, name='tambah_tool'),
    path('tool/<int:tool_id>/edit/', views.edit_tool, name='edit_tool'),
    path('tool/<int:tool_id>/delete/', views.hapus_tool, name='hapus_tool'),
    path('tool/<int:tool_id>/send_to_lab/', views.send_to_lab, name='send_to_lab'),
    path('lab/', views.lab_maintenance_list, name='lab_maintenance_list'),
    path('tool/<int:tool_id>/finish_repair/', views.finish_repair, name='finish_repair'),
    path('suku-cadang/', views.manajemen_stok, name='manajemen_stok'),
    path('laporan/', views.halaman_laporan, name='halaman_laporan'),
    path('laporan/download/', views.download_laporan_excel, name='download_laporan_excel'),
    path('produksi/', views.halaman_produksi, name='halaman_produksi'),
    path('hak-akses/', views.hak_akses_list, name='hak_akses_list'),
    path('hak-akses/<int:user_id>/edit/', views.edit_hak_akses, name='edit_hak_akses'),
    path('tool/<int:tool_id>/history/', views.get_tool_history, name='get_tool_history'),
    path('lab/download/', views.download_laporan_lab, name='download_laporan_lab'),
    path('suku-cadang/download/', views.download_laporan_stok, name='download_laporan_stok'),
    path('hak-akses/<int:user_id>/delete/', views.hapus_pengguna, name='hapus_pengguna'),
    path('proses/<int:proses_id>/hapus/', views.hapus_proses, name='hapus_proses'),
    path('gudang-tpm/', views.gudang_tpm_list, name='gudang_tpm_list'),
    path('repair/store/<int:tool_id>/', views.simpan_di_gudang, name='simpan_di_gudang'),
    path('gudang/hapus/<int:tool_id>/', views.hapus_tool_gudang, name='hapus_tool_gudang'),
    path('gudang/download/', views.download_gudang_excel, name='download_gudang_excel'),
    path('gudang/kembalikan/<int:tool_id>/', views.kembalikan_tool_gudang, name='kembalikan_tool_gudang'),
    path('gudang/kembalikan/<int:tool_id>/', views.kembalikan_ke_lab, name='kembalikan_tool_gudang'),
]