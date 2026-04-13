import pytest
from uuid import uuid4
from modules.epel.permohonan.domain.entities import Permohonan, Pemohon, StatusPermohonan
from modules.epel.permohonan.domain.value_objects import NIK, NomorPermohonan, JenisLayanan
from modules.epel.permohonan.domain.events import PermohonanDiajukan
from shared_kernel.domain.exceptions import BusinessRuleViolation


def make_permohonan(**overrides) -> Permohonan:
    defaults = dict(
        nomor=NomorPermohonan("PM-2026-000001"),
        pemohon=Pemohon(
            nik=NIK("3201010101010001"),
            nama_lengkap="Budi Santoso",
            nomor_hp="08123456789",
            alamat="Jl. Merdeka No. 1",
        ),
        jenis_layanan=JenisLayanan.from_code("KTP"),
    )
    defaults.update(overrides)
    return Permohonan(**defaults)


class TestNIK:
    def test_valid_nik(self):
        nik = NIK("3201010101010001")
        assert nik.value == "3201010101010001"

    def test_invalid_nik_too_short(self):
        with pytest.raises(ValueError, match="NIK tidak valid"):
            NIK("320101")

    def test_invalid_nik_non_digit(self):
        with pytest.raises(ValueError):
            NIK("320101ABCDEF0001")


class TestNomorPermohonan:
    def test_valid_format(self):
        nomor = NomorPermohonan("PM-2026-000001")
        assert str(nomor) == "PM-2026-000001"

    def test_invalid_format(self):
        with pytest.raises(ValueError):
            NomorPermohonan("INVALID")

    def test_generate(self):
        nomor = NomorPermohonan.generate(2026, 42)
        assert str(nomor) == "PM-2026-000042"


class TestPermohonanStateMachine:
    def test_draft_can_be_ajukan(self):
        p = make_permohonan()
        assert p.status == StatusPermohonan.DRAFT
        p.ajukan()
        assert p.status == StatusPermohonan.DIAJUKAN

    def test_ajukan_emits_event(self):
        p = make_permohonan()
        p.ajukan()
        events = p.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], PermohonanDiajukan)

    def test_pull_events_clears_them(self):
        p = make_permohonan()
        p.ajukan()
        p.pull_events()
        assert p.pull_events() == []

    def test_cannot_ajukan_twice(self):
        p = make_permohonan()
        p.ajukan()
        with pytest.raises(BusinessRuleViolation):
            p.ajukan()

    def test_full_happy_path(self):
        p = make_permohonan()
        p.ajukan()
        p.verifikasi()
        p.setujui(catatan="Dokumen lengkap")
        p.selesaikan()
        assert p.status == StatusPermohonan.SELESAI

    def test_tolak_requires_alasan(self):
        p = make_permohonan()
        p.ajukan()
        with pytest.raises(BusinessRuleViolation, match="Alasan penolakan wajib diisi"):
            p.tolak(alasan="")

    def test_tolak_sets_catatan(self):
        p = make_permohonan()
        p.ajukan()
        p.tolak(alasan="Dokumen tidak lengkap")
        assert p.status == StatusPermohonan.DITOLAK
        assert p.catatan_petugas == "Dokumen tidak lengkap"
