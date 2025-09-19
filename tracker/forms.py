# tracker/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tool, Proses, SukuCadang, ProductionLog, UserProfile

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
        # 'jumlah_shot' ditambahkan ke daftar ini
        fields = [
            'proses', 'stasiun', 'id_tool', 'tipe_tool', 
            'nomor_seri', 'jumlah_shot', 'max_shot', 'lifetime', 'jam_pakai_terakumulasi'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class MaintenanceForm(forms.ModelForm):
    proses = forms.ModelChoiceField(queryset=Proses.objects.all(), required=True, label="Kembalikan ke Proses", empty_label=None)
    # --- CHECKBOX BARU DITAMBAHKAN DI SINI ---
    reset_shot_terpakai = forms.BooleanField(label="Reset Shot Terpakai ke 0?", required=False)

    class Meta:
        model = Tool
        fields = ['jenis_kerusakan', 'part_yang_digunakan', 'proses']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Terapkan style ke field yang ada di Meta
        for field_name in self.Meta.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        # Terapkan style ke field custom (checkbox tidak perlu)
        self.fields['proses'].widget.attrs.update({'class': 'form-select'})

class StokMasukForm(forms.Form):
    nama_barang_baru = forms.CharField(label="Nama Barang Baru (jika tidak ada di daftar)", max_length=200, required=False)
    barang_yang_ada = forms.ModelChoiceField(label="Pilih Barang (jika sudah ada)", queryset=SukuCadang.objects.all(), required=False)
    jumlah = forms.IntegerField(min_value=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class StokKeluarForm(forms.Form):
    suku_cadang = forms.ModelChoiceField(label="Nama Barang", queryset=SukuCadang.objects.all(), empty_label=None)
    jumlah = forms.IntegerField(min_value=1)
    tujuan = forms.CharField(max_length=255)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProductionLogForm(forms.ModelForm):
    durasi_produksi = forms.FloatField(label="Durasi Produksi Hari Ini (Jam)", required=True, min_value=0)
    class Meta:
        model = ProductionLog
        fields = ['jumlah_produksi']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

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
        # Tambahkan 5 field baru
        fields = [
            'can_view_proses', 'can_edit_proses',
            'can_view_lab', 'can_edit_lab',
            'can_view_stok', 'can_edit_stok',
            'can_view_laporan', 'can_edit_laporan',
            'can_view_produksi', 'can_edit_produksi',
        ]