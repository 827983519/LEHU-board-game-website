"""
WSGI config for ECE651 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
#sys.path.append('/home/ubuntu/LEHU_env/lib/python3.6/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ECE651.settings')

application = get_wsgi_application()
