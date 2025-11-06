# tracker/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Pastikan semua model ini di-import
from .models import (
    Tool, Proses, SukuCadang, ProductionLog, 
    UserProfile, RiwayatPerbaikan, RiwayatStok
)

class ProsesForm(forms.ModelForm):
    class Meta:
        model = Proses
        fields = ['nama']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nama'].widget.attrs.update({
            'class': 'form-control',
            'id': 'id_nama_proses'
        })

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = [
            'proses', 'stasiun', 'id_tool', 'tipe_tool',
            'nomor_seri', 'jumlah_shot', 'max_shot', 'lifetime', 'jam_pakai_terakumulasi'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if field == 'proses':
                self.fields[field].widget.attrs.update({'class': 'form-select'})


# --- PERUBAHAN UTAMA DIMULAI DI SINI ---

# 1. FORM LAMA (MaintenanceForm): Sekarang hanya untuk "Menyelesaikan" perbaikan
class MaintenanceForm(forms.ModelForm):
    # Field 'proses' diganti namanya agar lebih jelas
    proses_tujuan = forms.ModelChoiceField(
        queryset=Proses.objects.all(), 
        required=True, 
        label="Kembalikan ke Proses Tujuan", 
        empty_label="-- Pilih Proses --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    reset_shot_terpakai = forms.BooleanField(
        label="Reset Shot Terpakai ke 0", 
        required=False
    )

    class Meta:
        model = RiwayatPerbaikan # Model diubah ke RiwayatPerbaikan
        fields = ['proses_tujuan', 'reset_shot_terpakai'] # Hanya berisi field untuk menyelesaikan


# 2. FORM BARU: Khusus untuk "Diagnosa" (Mengisi kerusakan dan part)
class UpdateDiagnosaForm(forms.ModelForm):
    class Meta:
        model = RiwayatPerbaikan # Model terhubung ke RiwayatPerbaikan
        fields = ['jenis_kerusakan', 'part_yang_digunakan']
        widgets = {
            'jenis_kerusakan': forms.TextInput(attrs={'class': 'form-control'}),
            'part_yang_digunakan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'jenis_kerusakan': "Jenis Kerusakan yang Ditemukan",
            'part_yang_digunakan': "Part yang Digunakan (Pisahkan dengan koma jika banyak)",
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Form ini wajib diisi untuk diagnosa
        self.fields['jenis_kerusakan'].required = True
        self.fields['part_yang_digunakan'].required = True

# --- PERUBAHAN UTAMA SELESAI ---


# Form Stok disederhanakan menggunakan ModelForm agar lebih konsisten
class StokMasukForm(forms.Form):
    nama = forms.CharField(
        label="Nama Suku Cadang (Baru atau Lama)", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    jumlah = forms.IntegerField(
        label="Jumlah Masuk", 
        min_value=1, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class StokKeluarForm(forms.ModelForm):
    class Meta:
        model = RiwayatStok
        fields = ['suku_cadang', 'jumlah', 'tujuan']
        labels = {
            'suku_cadang': 'Pilih Suku Cadang',
            'jumlah': 'Jumlah Keluar',
            'tujuan': 'Tujuan Pengambilan (Tool ID / Keperluan)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['suku_cadang'].widget.attrs.update({'class': 'form-select'})
        self.fields['jumlah'].widget.attrs.update({'class': 'form-control', 'min': 1})
        self.fields['tujuan'].widget.attrs.update({'class': 'form-control'})
        # Ambil queryset yang hanya menampilkan stok > 0, atau biarkan semua
        self.fields['suku_cadang'].queryset = SukuCadang.objects.order_by('nama')


class ProductionLogForm(forms.ModelForm):
    durasi_produksi = forms.FloatField(
        label="Durasi Produksi Hari Ini (Jam)", 
        required=True, 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ProductionLog
        fields = ['jumlah_produksi']
        labels = {
            'jumlah_produksi': 'Jumlah Produksi Selesai'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jumlah_produksi'].widget.attrs.update({'class': 'form-control', 'min': 1})


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nama_lengkap = forms.CharField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'nama_lengkap']
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        if commit:
            user.save()
            user.userprofile.nama_lengkap = self.cleaned_data.get('nama_lengkap')
            user.userprofile.save()
        return user

class PermissionsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'can_view_proses', 'can_edit_proses',
            'can_view_lab', 'can_edit_lab',
            'can_view_stok', 'can_edit_stok',
            'can_view_laporan', 'can_edit_laporan',
            'can_view_produksi', 'can_edit_produksi',
            'can_manage_gudang_tpm',
        ]
        # Membuat semua field tampil sebagai checkbox
        widgets = {
            'can_view_proses': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_edit_proses': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_view_lab': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_edit_lab': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_view_stok': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_edit_stok': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_view_laporan': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_edit_laporan': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_view_produksi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_edit_produksi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_gudang_tpm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StokHistoryFilterForm(forms.Form):
    start_date = forms.DateField(
        label="Dari Tanggal",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label="Sampai Tanggal",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )