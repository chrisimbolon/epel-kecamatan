"""
Queries are requests for data. They do NOT change state.
CQRS: read side can bypass the domain and go straight to ORM for performance.
"""
from __future__ import annotations
from uuid import UUID


def get_permohonan_ringkasan(permohonan_id: UUID) -> dict | None:
    """
    Read-side query: returns a lightweight summary dict.
    Bypasses domain entities — reads directly from ORM for speed.
    Called by other bounded contexts via the facade.
    """
    # Import ORM here — this is infrastructure, not domain
    from modules.epel.permohonan.infrastructure.models import PermohonanORM
    try:
        orm = PermohonanORM.objects.values(
            "id", "nomor", "status", "jenis_layanan_code", "created_at"
        ).get(id=permohonan_id)
        return dict(orm)
    except PermohonanORM.DoesNotExist:
        return None
