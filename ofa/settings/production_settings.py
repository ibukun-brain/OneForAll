from .base_settings import *

MIDDLEWARE += [
    "x_forwarded_for.middleware.XForwardedForMiddleware" #for production on nginx
] 

