# tracker/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Proses(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nama

class Tool(models.Model):
    proses = models.ForeignKey(Proses, on_delete=models.SET_NULL, null=True, blank=True)
    stasiun = models.CharField(max_length=50)
    id_tool = models.CharField("ID Tool", max_length=50, unique=True)
    tipe_tool = models.CharField("Tipe Tool", max_length=100)
    nomor_seri = models.CharField("Nomor Seri", max_length=100)
    jumlah_shot = models.IntegerField("Shot per Produksi", default=1)
    max_shot = models.IntegerField("Max Shot", default=0)
    shot_terpakai = models.IntegerField("Shot Terpakai", default=0)
    lifetime = models.IntegerField("Lifetime (hari)", default=365)
    STATUS_CHOICES = [('Tersedia', 'Tersedia'), ('Dipakai', 'Dipakai'), ('Perbaikan', 'Dalam Perbaikan')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Tersedia')
    jenis_kerusakan = models.CharField(max_length=255, blank=True, null=True, help_text="Diisi saat tool masuk lab")
    part_yang_digunakan = models.TextField(blank=True, null=True, help_text="Part yang diganti atau diperbaiki")
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diupdate_pada = models.DateTimeField(auto_now=True)
    def __str__(self): return self.id_tool
    @property
    def sisa_shot(self): return self.max_shot - self.shot_terpakai
    @property
    def performa(self):
        if self.max_shot > 0: return round((self.sisa_shot / self.max_shot) * 100)
        return 0

class SukuCadang(models.Model):
    nama = models.CharField(max_length=200, unique=True)
    jumlah_stok = models.IntegerField(default=0)
    def __str__(self): return f"{self.nama} (Stok: {self.jumlah_stok})"

class RiwayatStok(models.Model):
    STATUS_CHOICES = [('Masuk', 'Masuk'), ('Keluar', 'Keluar')]
    suku_cadang = models.ForeignKey(SukuCadang, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    tujuan = models.CharField(max_length=255, blank=True, null=True)
    nama_pengguna = models.CharField(max_length=150)
    waktu = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.waktu.strftime('%Y-%m-%d %H:%M')} - {self.suku_cadang.nama} - {self.status} ({self.jumlah})"

class ProductionLog(models.Model):
    # Field 'proses' kita hapus dari sini
    jumlah_produksi = models.PositiveIntegerField()
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Teks diubah karena tidak ada lagi info proses
        return f"Produksi {self.jumlah_produksi} pada {self.dibuat_pada.strftime('%Y-%m-%d')}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=100)
    is_developer = models.BooleanField(default=False)

    # Nama field diubah agar lebih jelas
    can_view_proses = models.BooleanField(default=False, verbose_name="Lihat Menu Proses")
    can_view_lab = models.BooleanField(default=False, verbose_name="Lihat Menu Lab")
    can_view_stok = models.BooleanField(default=False, verbose_name="Lihat Menu Stok")
    can_view_laporan = models.BooleanField(default=False, verbose_name="Lihat Menu Laporan")
    can_view_produksi = models.BooleanField(default=False, verbose_name="Lihat Menu Produksi")

    # --- FIELD BARU UNTUK AKSES PENUH (EDIT/DELETE/ADD) ---
    can_edit_proses = models.BooleanField(default=False, verbose_name="Akses Penuh Menu Proses")
    can_edit_lab = models.BooleanField(default=False, verbose_name="Akses Penuh Menu Lab")
    can_edit_stok = models.BooleanField(default=False, verbose_name="Akses Penuh Menu Stok")
    can_edit_laporan = models.BooleanField(default=False, verbose_name="Akses Penuh Menu Laporan (Termasuk Download)")
    can_edit_produksi = models.BooleanField(default=False, verbose_name="Akses Penuh Menu Produksi")

    def __str__(self):
        return self.user.username

class RiwayatPerbaikan(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='riwayat_perbaikan')
    waktu_selesai = models.DateTimeField(auto_now_add=True)
    jenis_kerusakan = models.CharField(max_length=255)
    part_yang_digunakan = models.TextField()
    dikerjakan_oleh = models.CharField(max_length=150)
    def __str__(self): return f"Perbaikan {self.tool.id_tool} pada {self.waktu_selesai.strftime('%Y-%m-%d')}"

class RiwayatPerbaikan(models.Model):
    STATUS_CHOICES = [
        ('Sedang Diperbaiki', 'Sedang Diperbaiki'),
        ('Selesai', 'Selesai'),
    ]
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='riwayat_perbaikan')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Sedang Diperbaiki')
    
    # Waktu akan kita atur melalui view
    waktu_masuk = models.DateTimeField()
    waktu_selesai = models.DateTimeField(null=True, blank=True)
    
    # Detail perbaikan, bisa kosong saat baru masuk
    jenis_kerusakan = models.CharField(max_length=255, null=True, blank=True)
    part_yang_digunakan = models.TextField(null=True, blank=True)
    dikerjakan_oleh = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"Perbaikan {self.tool.id_tool} pada {self.waktu_masuk.strftime('%Y-%m-%d')}"