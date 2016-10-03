# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 14/09/16.

import os

if os.getenv("SERVER_ENV", "DEVEL") == "DEVEL":
    from .development import *
elif os.getenv("SERVER_ENV", "DEVEL") == "PROD":
    from .production import *

