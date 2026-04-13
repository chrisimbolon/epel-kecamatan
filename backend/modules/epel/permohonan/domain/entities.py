from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

from shared_kernel.domain.aggregate import AggregateRoot
from shared_kernel.domain.entity import Entity
from shared_kernel.domain.exceptions import BusinessRuleViolation
from .value_objects import NIK, NomorPermohonan, JenisLayanan
from .events import PermohonanDiajukan, PermohonanDisetujui, PermohonanDitolak


class StatusPermohonan(str, Enum):
    DRAFT        = "draft"
    DIAJUKAN     = "diajukan"
    DIVERIFIKASI = "diverifikasi"
    DISETUJUI    = "disetujui"
    DITOLAK      = "ditolak"
    SELESAI      = "selesai"


@dataclass
class Pemohon(Entity):
    nik:          NIK  = field(kw_only=True)
    nama_lengkap: str  = field(kw_only=True)
    nomor_hp:     str  = field(kw_only=True)
    alamat:       str  = field(kw_only=True)


@dataclass
class Permohonan(AggregateRoot):
    nomor:           NomorPermohonan  = field(kw_only=True)
    pemohon:         Pemohon          = field(kw_only=True)
    jenis_layanan:   JenisLayanan     = field(kw_only=True)
    status:          StatusPermohonan = field(default=StatusPermohonan.DRAFT, kw_only=True)
    catatan_petugas: str              = field(default="", kw_only=True)

    def ajukan(self) -> None:
        if self.status != StatusPermohonan.DRAFT:
            raise BusinessRuleViolation(
                f"Permohonan {self.nomor} tidak bisa diajukan dari status {self.status.value}"
            )
        self.status = StatusPermohonan.DIAJUKAN
        self.register_event(PermohonanDiajukan(
            permohonan_id=self.id,
            nomor=str(self.nomor),
            nik=str(self.pemohon.nik),
            jenis_layanan=self.jenis_layanan.code,
        ))

    def verifikasi(self) -> None:
        if self.status != StatusPermohonan.DIAJUKAN:
            raise BusinessRuleViolation("Hanya permohonan berstatus DIAJUKAN yang bisa diverifikasi")
        self.status = StatusPermohonan.DIVERIFIKASI

    def setujui(self, catatan: str = "") -> None:
        if self.status != StatusPermohonan.DIVERIFIKASI:
            raise BusinessRuleViolation("Hanya permohonan berstatus DIVERIFIKASI yang bisa disetujui")
        self.status = StatusPermohonan.DISETUJUI
        self.catatan_petugas = catatan
        self.register_event(PermohonanDisetujui(
            permohonan_id=self.id,
            nomor=str(self.nomor),
        ))

    def tolak(self, alasan: str) -> None:
        if self.status not in (StatusPermohonan.DIAJUKAN, StatusPermohonan.DIVERIFIKASI):
            raise BusinessRuleViolation("Status tidak memungkinkan penolakan")
        if not alasan.strip():
            raise BusinessRuleViolation("Alasan penolakan wajib diisi")
        self.status = StatusPermohonan.DITOLAK
        self.catatan_petugas = alasan
        self.register_event(PermohonanDitolak(
            permohonan_id=self.id,
            nomor=str(self.nomor),
            alasan=alasan,
        ))

    def selesaikan(self) -> None:
        if self.status != StatusPermohonan.DISETUJUI:
            raise BusinessRuleViolation("Hanya permohonan DISETUJUI yang bisa diselesaikan")
        self.status = StatusPermohonan.SELESAI
