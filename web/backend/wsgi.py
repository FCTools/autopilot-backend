# Copyright © 2020-2021 Filthy Claws Tools - All Rights Reserved
#
# This file is part of autopilot.autopilot-backend.
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Author: German Yakimov <german13yakimov@gmail.com>

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('..')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.prod')

application = get_wsgi_application()
