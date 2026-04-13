"""
API views — thin layer. Validate → call use case → return response.
No business logic. No direct ORM access.
"""
from __future__ import annotations
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    BuatPermohonanSerializer,
    PermohonanResponseSerializer,
    AksiPermohonanSerializer,
)
from ...application.commands import (
    BuatPermohonanCommand,
    AjukanPermohonanCommand,
    SetujuiPermohonanCommand,
    TolakPermohonanCommand,
)
from ...application.container import (
    get_buat_use_case,
    get_ajukan_use_case,
    get_setujui_use_case,
    get_tolak_use_case,
)


class PermohonanListCreateView(APIView):
    def post(self, request):
        serializer = BuatPermohonanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cmd = BuatPermohonanCommand(**serializer.validated_data)
        result = get_buat_use_case().execute(cmd)
        if result.is_failure:
            return Response({"detail": result.error}, status=status.HTTP_400_BAD_REQUEST)
        out = PermohonanResponseSerializer(result.value)
        return Response(out.data, status=status.HTTP_201_CREATED)


class AjukanPermohonanView(APIView):
    def post(self, request, permohonan_id: str):
        result = get_ajukan_use_case().execute(
            AjukanPermohonanCommand(permohonan_id=permohonan_id)
        )
        if result.is_failure:
            return Response({"detail": result.error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": result.value.status.value})


class SetujuiPermohonanView(APIView):
    def post(self, request, permohonan_id: str):
        serializer = AksiPermohonanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = get_setujui_use_case().execute(
            SetujuiPermohonanCommand(
                permohonan_id=permohonan_id,
                catatan=serializer.validated_data["catatan"],
            )
        )
        if result.is_failure:
            return Response({"detail": result.error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": result.value.status.value})


class TolakPermohonanView(APIView):
    def post(self, request, permohonan_id: str):
        serializer = AksiPermohonanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        alasan = serializer.validated_data.get("alasan", "")
        if not alasan:
            return Response({"detail": "Alasan wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)
        result = get_tolak_use_case().execute(
            TolakPermohonanCommand(
                permohonan_id=permohonan_id,
                alasan=alasan,
            )
        )
        if result.is_failure:
            return Response({"detail": result.error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": result.value.status.value})
