"""
Commands are intentions to change state. Immutable input objects.
Named in imperative form: Verb + Noun.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class BuatPermohonanCommand:
    nik: str
    nama_lengkap: str
    nomor_hp: str
    alamat: str
    jenis_layanan_code: str


@dataclass(frozen=True)
class AjukanPermohonanCommand:
    permohonan_id: str


@dataclass(frozen=True)
class SetujuiPermohonanCommand:
    permohonan_id: str
    catatan: str = ""


@dataclass(frozen=True)
class TolakPermohonanCommand:
    permohonan_id: str
    alasan: str
