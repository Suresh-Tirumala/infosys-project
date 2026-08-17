import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

# Run migrations on cold start for serverless environments
from django.core.management import call_command
call_command('migrate', '--run-syncdb', verbosity=0)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
