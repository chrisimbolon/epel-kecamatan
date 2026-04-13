"""
Dependency wiring for the permohonan use cases.
Views call get_*_use_case() instead of instantiating dependencies themselves.
Swap implementations here (e.g. for testing) without touching views.
"""
from __future__ import annotations
from .use_cases import (
    BuatPermohonanUseCase,
    AjukanPermohonanUseCase,
    SetujuiPermohonanUseCase,
    TolakPermohonanUseCase,
)
from .event_publisher import DjangoSignalEventPublisher
from ..infrastructure.orm_repositories import DjangoPermohonanRepository


def _repo():
    return DjangoPermohonanRepository()

def _publisher():
    return DjangoSignalEventPublisher()


def get_buat_use_case()    -> BuatPermohonanUseCase:
    return BuatPermohonanUseCase(_repo(), _publisher())

def get_ajukan_use_case()  -> AjukanPermohonanUseCase:
    return AjukanPermohonanUseCase(_repo(), _publisher())

def get_setujui_use_case() -> SetujuiPermohonanUseCase:
    return SetujuiPermohonanUseCase(_repo(), _publisher())

def get_tolak_use_case()   -> TolakPermohonanUseCase:
    return TolakPermohonanUseCase(_repo(), _publisher())
