"""
Event publisher interface + Django signals implementation.
The application layer depends on the interface; infrastructure provides the impl.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from django.dispatch import Signal
from shared_kernel.domain.events import DomainEvent

# Django signals — other apps subscribe to these
permohonan_diajukan    = Signal()
permohonan_disetujui   = Signal()
permohonan_ditolak     = Signal()


class EventPublisher(ABC):
    @abstractmethod
    def publish_all(self, events: list[DomainEvent]) -> None: ...


class DjangoSignalEventPublisher(EventPublisher):
    """Routes domain events to Django signals."""

    _SIGNAL_MAP = {
        "PermohonanDiajukan":  permohonan_diajukan,
        "PermohonanDisetujui": permohonan_disetujui,
        "PermohonanDitolak":   permohonan_ditolak,
    }

    def publish_all(self, events: list[DomainEvent]) -> None:
        for event in events:
            signal = self._SIGNAL_MAP.get(event.event_type)
            if signal:
                signal.send(sender=self.__class__, event=event)
