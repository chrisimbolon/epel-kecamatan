"""Django admin for permohonan — ops and backoffice use only."""
from django.contrib import admin
from .models import PermohonanORM, PemohonORM


@admin.register(PemohonORM)
class PemohonAdmin(admin.ModelAdmin):
    list_display  = ("nama_lengkap", "nik", "nomor_hp", "created_at")
    search_fields = ("nama_lengkap", "nik")
    readonly_fields = ("id", "created_at")


@admin.register(PermohonanORM)
class PermohonanAdmin(admin.ModelAdmin):
    list_display   = ("nomor", "status", "jenis_layanan_code", "created_at", "updated_at")
    list_filter    = ("status", "jenis_layanan_code")
    search_fields  = ("nomor", "pemohon__nama_lengkap", "pemohon__nik")
    readonly_fields = ("id", "nomor", "created_at", "updated_at")
    ordering       = ("-created_at",)
