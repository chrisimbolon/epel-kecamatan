"""
Use cases orchestrate domain operations.
They do NOT contain business logic — they delegate to domain entities.
Each use case = one public action in the system.
"""
from __future__ import annotations
from datetime import date
from uuid import UUID

from shared_kernel.domain.result import Result
from shared_kernel.domain.exceptions import EntityNotFound, BusinessRuleViolation
from ..domain.entities import Permohonan, Pemohon
from ..domain.repositories import PermohonanRepository
from ..domain.value_objects import NIK, NomorPermohonan, JenisLayanan
from .commands import (
    BuatPermohonanCommand,
    AjukanPermohonanCommand,
    SetujuiPermohonanCommand,
    TolakPermohonanCommand,
)
from .event_publisher import EventPublisher


class BuatPermohonanUseCase:
    def __init__(self, repo: PermohonanRepository, publisher: EventPublisher) -> None:
        self._repo = repo
        self._publisher = publisher

    def execute(self, cmd: BuatPermohonanCommand) -> Result[Permohonan]:
        try:
            nik = NIK(cmd.nik)
            jenis = JenisLayanan.from_code(cmd.jenis_layanan_code)
            seq = self._repo.next_sequence_number(date.today().year)
            nomor = NomorPermohonan.generate(date.today().year, seq)
            pemohon = Pemohon(
                nik=nik,
                nama_lengkap=cmd.nama_lengkap,
                nomor_hp=cmd.nomor_hp,
                alamat=cmd.alamat,
            )
            permohonan = Permohonan(nomor=nomor, pemohon=pemohon, jenis_layanan=jenis)
            self._repo.save(permohonan)
            self._publisher.publish_all(permohonan.pull_events())
            return Result.ok(permohonan)
        except (ValueError, BusinessRuleViolation) as e:
            return Result.fail(str(e))


class AjukanPermohonanUseCase:
    def __init__(self, repo: PermohonanRepository, publisher: EventPublisher) -> None:
        self._repo = repo
        self._publisher = publisher

    def execute(self, cmd: AjukanPermohonanCommand) -> Result[Permohonan]:
        permohonan = self._repo.get_by_id(UUID(cmd.permohonan_id))
        if permohonan is None:
            return Result.fail(f"Permohonan {cmd.permohonan_id} tidak ditemukan")
        try:
            permohonan.ajukan()
            self._repo.save(permohonan)
            self._publisher.publish_all(permohonan.pull_events())
            return Result.ok(permohonan)
        except BusinessRuleViolation as e:
            return Result.fail(str(e))


class SetujuiPermohonanUseCase:
    def __init__(self, repo: PermohonanRepository, publisher: EventPublisher) -> None:
        self._repo = repo
        self._publisher = publisher

    def execute(self, cmd: SetujuiPermohonanCommand) -> Result[Permohonan]:
        permohonan = self._repo.get_by_id(UUID(cmd.permohonan_id))
        if permohonan is None:
            return Result.fail(f"Permohonan {cmd.permohonan_id} tidak ditemukan")
        try:
            permohonan.setujui(cmd.catatan)
            self._repo.save(permohonan)
            self._publisher.publish_all(permohonan.pull_events())
            return Result.ok(permohonan)
        except BusinessRuleViolation as e:
            return Result.fail(str(e))


class TolakPermohonanUseCase:
    def __init__(self, repo: PermohonanRepository, publisher: EventPublisher) -> None:
        self._repo = repo
        self._publisher = publisher

    def execute(self, cmd: TolakPermohonanCommand) -> Result[Permohonan]:
        permohonan = self._repo.get_by_id(UUID(cmd.permohonan_id))
        if permohonan is None:
            return Result.fail(f"Permohonan {cmd.permohonan_id} tidak ditemukan")
        try:
            permohonan.tolak(cmd.alasan)
            self._repo.save(permohonan)
            self._publisher.publish_all(permohonan.pull_events())
            return Result.ok(permohonan)
        except BusinessRuleViolation as e:
            return Result.fail(str(e))
