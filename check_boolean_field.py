import os
import sys
import django
from django.conf import settings

# Configure Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'core',
    ],
    USE_I18N=True,
)

django.setup()

from django.db import models

# Check BooleanField signature
print("BooleanField init signature:")
print(models.BooleanField.__init__.__annotations__)