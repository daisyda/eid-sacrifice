from django.apps import AppConfig

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
<<<<<<< HEAD
    name = 'main_app'

    def ready(self):
        from . import fix_status
        fix_status.fix_status_values()
=======
    name = 'main_app'  # make sure this matches your folder name exactly

    def ready(self):
        import main_app.signals  # 🔥 this line activates your status change hook
>>>>>>> bc55f73 (Register Udhiyah and update load/fix views)
