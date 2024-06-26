"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application


path = '/home/sohy3110/my-first-blog'
if path not in sys.path:
    sys.path.append(path)

activate_env = os.path.expanduser('/home/sohy3110/my-first-blog/myvenv/bin/activate_this.py')
with open(activate_env) as f:
    exec(f.read(), dict(__file__=activate_env))

os.environ['DJANGO_SETTINGS_MODULE'] =  'mysite.settings'
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())
