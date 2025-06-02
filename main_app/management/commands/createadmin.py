from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a default admin user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = 'adminpassword123'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('✅ Superuser created'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Superuser already exists'))
