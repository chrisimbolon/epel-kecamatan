"""
Signal handlers — other bounded contexts react to permohonan events here.
Import is triggered by PermohonanConfig.ready().
"""
from __future__ import annotations
# from modules.epel.notifications import notify_pemohon_diajukan  # example


def on_permohonan_diajukan(sender, event, **kwargs) -> None:
    """Triggered when a permohonan moves to DIAJUKAN status."""
    # e.g. send SMS, log audit trail, notify supervisor
    pass


def on_permohonan_disetujui(sender, event, **kwargs) -> None:
    pass


def on_permohonan_ditolak(sender, event, **kwargs) -> None:
    pass


# Wire up signals
from modules.epel.permohonan.application.event_publisher import (
    permohonan_diajukan,
    permohonan_disetujui,
    permohonan_ditolak,
)

permohonan_diajukan.connect(on_permohonan_diajukan)
permohonan_disetujui.connect(on_permohonan_disetujui)
permohonan_ditolak.connect(on_permohonan_ditolak)
