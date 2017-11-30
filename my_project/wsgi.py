"""
WSGI config for my_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import site

from django.core.wsgi import get_wsgi_application

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/html/ppa-iitb/my_project/ppaenv/lib/python3.5/site-packages/')

DJANGO_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
# Add the app's directory to the PYTHONPATH
sys.path.append(DJANGO_PATH)
sys.path.append('/var/www/html/ppa-iitb/my_project')
sys.path.append('/var/www/html/ppa-iitb/my_project/my_project')

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

# Activate your virtual env
#activate_env=os.path.expanduser("/var/www/html/ppa-iitb/mysite/ppaenv/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

application = get_wsgi_application()
#import django.core.handlers.wsgi
#application= django.core.handlers.wsgi.WSGIHandler()
