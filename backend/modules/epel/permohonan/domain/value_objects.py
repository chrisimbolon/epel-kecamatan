"""
Permohonan value objects.
No Django imports. Pure Python. Testable with plain pytest.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from shared_kernel.domain.value_object import ValueObject


@dataclass(frozen=True)
class NIK(ValueObject):
    """Nomor Induk Kependudukan — 16-digit national ID."""
    value: str

    def __post_init__(self) -> None:
        if not re.match(r"^\d{16}$", self.value):
            raise ValueError(f"NIK tidak valid: {self.value!r}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class NomorPermohonan(ValueObject):
    """Format: PM-YYYY-NNNNNN e.g. PM-2026-000001"""
    value: str

    def __post_init__(self) -> None:
        if not re.match(r"^PM-\d{4}-\d{6}$", self.value):
            raise ValueError(f"Format nomor permohonan tidak valid: {self.value!r}")

    def __str__(self) -> str:
        return self.value

    @classmethod
    def generate(cls, year: int, sequence: int) -> "NomorPermohonan":
        return cls(value=f"PM-{year}-{sequence:06d}")


@dataclass(frozen=True)
class JenisLayanan(ValueObject):
    code: str
    label: str

    CHOICES = {
        "KTP": "Kartu Tanda Penduduk",
        "KK":  "Kartu Keluarga",
        "SKD": "Surat Keterangan Domisili",
        "SKL": "Surat Keterangan Lahir",
        "SKM": "Surat Keterangan Meninggal",
        "IMB": "Izin Mendirikan Bangunan",
    }

    def __post_init__(self) -> None:
        if self.code not in self.CHOICES:
            raise ValueError(f"Jenis layanan tidak dikenal: {self.code!r}")

    @classmethod
    def from_code(cls, code: str) -> "JenisLayanan":
        return cls(code=code, label=cls.CHOICES[code])
