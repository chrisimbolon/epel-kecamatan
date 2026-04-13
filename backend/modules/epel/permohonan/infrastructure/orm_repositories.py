"""Concrete repository implementation using Django ORM."""
from __future__ import annotations
from uuid import UUID
from django.db import transaction
from ..domain.entities import Permohonan, StatusPermohonan
from ..domain.repositories import PermohonanRepository
from .models import PermohonanORM, PemohonORM
from .mappers import PermohonanMapper, PemohonMapper


class DjangoPermohonanRepository(PermohonanRepository):

    def get_by_id(self, id: UUID) -> Permohonan | None:
        try:
            orm = PermohonanORM.objects.select_related("pemohon").get(id=id)
            return PermohonanMapper.to_domain(orm)
        except PermohonanORM.DoesNotExist:
            return None

    def get_by_nomor(self, nomor: str) -> Permohonan | None:
        try:
            orm = PermohonanORM.objects.select_related("pemohon").get(nomor=nomor)
            return PermohonanMapper.to_domain(orm)
        except PermohonanORM.DoesNotExist:
            return None

    def list_by_status(self, status: StatusPermohonan) -> list[Permohonan]:
        qs = PermohonanORM.objects.select_related("pemohon").filter(status=status.value)
        return [PermohonanMapper.to_domain(orm) for orm in qs]

    @transaction.atomic
    def save(self, entity: Permohonan) -> None:
        pemohon_orm = PemohonMapper.to_orm(entity.pemohon)
        PemohonORM.objects.update_or_create(
            id=pemohon_orm.id,
            defaults={
                "nik": pemohon_orm.nik,
                "nama_lengkap": pemohon_orm.nama_lengkap,
                "nomor_hp": pemohon_orm.nomor_hp,
                "alamat": pemohon_orm.alamat,
            },
        )
        permohonan_orm = PermohonanMapper.to_orm(entity)
        PermohonanORM.objects.update_or_create(
            id=permohonan_orm.id,
            defaults={
                "nomor": permohonan_orm.nomor,
                "pemohon_id": entity.pemohon.id,
                "jenis_layanan_code": permohonan_orm.jenis_layanan_code,
                "jenis_layanan_label": permohonan_orm.jenis_layanan_label,
                "status": permohonan_orm.status,
                "catatan_petugas": permohonan_orm.catatan_petugas,
            },
        )

    def delete(self, id: UUID) -> None:
        PermohonanORM.objects.filter(id=id).delete()

    def next_sequence_number(self, year: int) -> int:
        count = PermohonanORM.objects.filter(nomor__startswith=f"PM-{year}-").count()
        return count + 1
