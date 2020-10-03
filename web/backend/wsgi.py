"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('..')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')

application = get_wsgi_application()
