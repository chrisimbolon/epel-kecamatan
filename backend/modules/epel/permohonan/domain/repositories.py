"""
Abstract repository interfaces for the permohonan context.
The domain declares WHAT it needs. Infrastructure delivers HOW.
"""
from __future__ import annotations
from abc import abstractmethod
from uuid import UUID
from shared_kernel.infrastructure.base_repository import Repository
from .entities import Permohonan, StatusPermohonan


class PermohonanRepository(Repository[Permohonan]):
    @abstractmethod
    def get_by_nomor(self, nomor: str) -> Permohonan | None: ...

    @abstractmethod
    def list_by_status(self, status: StatusPermohonan) -> list[Permohonan]: ...

    @abstractmethod
    def next_sequence_number(self, year: int) -> int:
        """Returns the next available sequence number for NomorPermohonan."""
        ...
