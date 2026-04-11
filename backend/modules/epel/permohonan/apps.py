from django.apps import AppConfig


class PermohonanConfig(AppConfig):
    name = "modules.epel.permohonan"
    label = "permohonan"
    verbose_name = "Permohonan Layanan"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        # Wire up signal handlers when Django starts
        import modules.epel.permohonan.infrastructure.signals  # noqa: F401
