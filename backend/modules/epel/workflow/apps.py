from django.apps import AppConfig


class WorkflowConfig(AppConfig):
    name = "modules.epel.workflow"
    label = "workflow"
    verbose_name = "Workflow dan Approval"
    default_auto_field = "django.db.models.BigAutoField"
