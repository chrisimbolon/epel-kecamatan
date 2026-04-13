"""
Django ORM models for permohonan.
These are PERSISTENCE models only — not domain entities.
No business logic here. No domain methods.
"""
import uuid
from django.db import models


class PemohonORM(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nik           = models.CharField(max_length=16, db_index=True)
    nama_lengkap  = models.CharField(max_length=255)
    nomor_hp      = models.CharField(max_length=20)
    alamat        = models.TextField()
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "permohonan"
        db_table  = "permohonan_pemohon"

    def __str__(self) -> str:
        return f"{self.nama_lengkap} ({self.nik})"


class PermohonanORM(models.Model):
    STATUS_CHOICES = [
        ("draft",        "Draft"),
        ("diajukan",     "Diajukan"),
        ("diverifikasi", "Diverifikasi"),
        ("disetujui",    "Disetujui"),
        ("ditolak",      "Ditolak"),
        ("selesai",      "Selesai"),
    ]

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nomor               = models.CharField(max_length=20, unique=True, db_index=True)
    pemohon             = models.ForeignKey(PemohonORM, on_delete=models.PROTECT, related_name="permohonan")
    jenis_layanan_code  = models.CharField(max_length=10, db_index=True)
    jenis_layanan_label = models.CharField(max_length=100)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft", db_index=True)
    catatan_petugas     = models.TextField(blank=True, default="")
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "permohonan"
        db_table  = "permohonan_permohonan"
        ordering  = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.nomor} [{self.status}]"
