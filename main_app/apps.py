from django.apps import AppConfig

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'  # make sure this matches your folder name exactly

    def ready(self):
        # ✅ Optional: Normalize statuses at startup
        from main_app.utils import fix_status
        fix_status.fix_status_values()

        # ✅ Optional: Connect model signal handlers
        import main_app.signals
