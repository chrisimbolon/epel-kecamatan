"""
Mappers: translate between ORM models and domain entities.
This is the Anti-Corruption Layer between persistence and domain.
"""
from __future__ import annotations
from ..domain.entities import Permohonan, Pemohon, StatusPermohonan
from ..domain.value_objects import NIK, NomorPermohonan, JenisLayanan
from .models import PermohonanORM, PemohonORM


class PemohonMapper:
    @staticmethod
    def to_domain(orm: PemohonORM) -> Pemohon:
        return Pemohon(
            id=orm.id,
            nik=NIK(orm.nik),
            nama_lengkap=orm.nama_lengkap,
            nomor_hp=orm.nomor_hp,
            alamat=orm.alamat,
        )

    @staticmethod
    def to_orm(entity: Pemohon) -> PemohonORM:
        return PemohonORM(
            id=entity.id,
            nik=entity.nik.value,
            nama_lengkap=entity.nama_lengkap,
            nomor_hp=entity.nomor_hp,
            alamat=entity.alamat,
        )


class PermohonanMapper:
    @staticmethod
    def to_domain(orm: PermohonanORM) -> Permohonan:
        pemohon = PemohonMapper.to_domain(orm.pemohon)
        return Permohonan(
            id=orm.id,
            nomor=NomorPermohonan(orm.nomor),
            pemohon=pemohon,
            jenis_layanan=JenisLayanan(
                code=orm.jenis_layanan_code,
                label=orm.jenis_layanan_label,
            ),
            status=StatusPermohonan(orm.status),
            catatan_petugas=orm.catatan_petugas,
        )

    @staticmethod
    def to_orm(entity: Permohonan) -> PermohonanORM:
        return PermohonanORM(
            id=entity.id,
            nomor=entity.nomor.value,
            jenis_layanan_code=entity.jenis_layanan.code,
            jenis_layanan_label=entity.jenis_layanan.label,
            status=entity.status.value,
            catatan_petugas=entity.catatan_petugas,
        )
