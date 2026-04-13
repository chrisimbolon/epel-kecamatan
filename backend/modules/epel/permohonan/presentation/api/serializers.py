"""DRF serializers = input/output DTOs for the API presentation layer."""
from rest_framework import serializers


class BuatPermohonanSerializer(serializers.Serializer):
    nik              = serializers.CharField(min_length=16, max_length=16)
    nama_lengkap     = serializers.CharField(max_length=255)
    nomor_hp         = serializers.CharField(max_length=20)
    alamat           = serializers.CharField()
    jenis_layanan_code = serializers.ChoiceField(choices=[
        "KTP", "KK", "SKD", "SKL", "SKM", "IMB"
    ])


class PermohonanResponseSerializer(serializers.Serializer):
    id               = serializers.UUIDField()
    nomor            = serializers.CharField()
    status           = serializers.CharField()
    jenis_layanan    = serializers.CharField(source="jenis_layanan.label")
    pemohon_nama     = serializers.CharField(source="pemohon.nama_lengkap")
    pemohon_nik      = serializers.CharField(source="pemohon.nik.value")


class AksiPermohonanSerializer(serializers.Serializer):
    """For approve/reject actions."""
    catatan = serializers.CharField(required=False, default="")
    alasan  = serializers.CharField(required=False, default="")
