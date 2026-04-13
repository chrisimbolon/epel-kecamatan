from django.urls import path
from .views import (
    PermohonanListCreateView,
    AjukanPermohonanView,
    SetujuiPermohonanView,
    TolakPermohonanView,
)

urlpatterns = [
    path("",                                   PermohonanListCreateView.as_view(), name="permohonan-list-create"),
    path("<str:permohonan_id>/ajukan/",        AjukanPermohonanView.as_view(),    name="permohonan-ajukan"),
    path("<str:permohonan_id>/setujui/",       SetujuiPermohonanView.as_view(),   name="permohonan-setujui"),
    path("<str:permohonan_id>/tolak/",         TolakPermohonanView.as_view(),     name="permohonan-tolak"),
]
