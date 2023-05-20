# flake8: noqa

from .base import *

""" INSTALLED_APPS += ["debug_toolbar"]

# INSTALLED_APPS += ["django.contrib.staticfiles"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
 """

# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"