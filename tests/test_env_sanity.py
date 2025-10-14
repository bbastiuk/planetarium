from django.conf import settings;import os;print('ENV =',os.environ.get('DJANGO_SETTINGS_MODULE'));print('SETTINGS =',settings.SETTINGS_MODULE);print('DB =',settings.DATABASES['default']['ENGINE'])
