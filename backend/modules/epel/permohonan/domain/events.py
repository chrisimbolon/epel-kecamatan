from __future__ import annotations
from dataclasses import dataclass, field
from uuid import UUID
from shared_kernel.domain.events import DomainEvent


@dataclass(frozen=True)
class PermohonanDiajukan(DomainEvent):
    permohonan_id: UUID = field(default=None, kw_only=True)
    nomor:         str  = field(default="",   kw_only=True)
    nik:           str  = field(default="",   kw_only=True)
    jenis_layanan: str  = field(default="",   kw_only=True)


@dataclass(frozen=True)
class PermohonanDisetujui(DomainEvent):
    permohonan_id: UUID = field(default=None, kw_only=True)
    nomor:         str  = field(default="",   kw_only=True)


@dataclass(frozen=True)
class PermohonanDitolak(DomainEvent):
    permohonan_id: UUID = field(default=None, kw_only=True)
    nomor:         str  = field(default="",   kw_only=True)
    alasan:        str  = field(default="",   kw_only=True)


@dataclass(frozen=True)
class IzinDiterbitkan(DomainEvent):
    permohonan_id:  UUID = field(default=None, kw_only=True)
    nomor:          str  = field(default="",   kw_only=True)
    nomor_dokumen:  str  = field(default="",   kw_only=True)
