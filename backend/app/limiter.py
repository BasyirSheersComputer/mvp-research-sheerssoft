
from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize limiter with default key function (remote IP)
# Global limit: 60 requests per minute per IP (generous default)
# Specific endpoints will have tighter or looser limits.
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
