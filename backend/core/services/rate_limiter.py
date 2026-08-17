import time
from collections import defaultdict
from django.conf import settings


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def is_rate_limited(self, key: str, limit: int = None) -> bool:
        limit = limit or settings.RATE_LIMIT_PER_MINUTE
        now = time.time()
        window = 60

        self.requests[key] = [t for t in self.requests[key] if now - t < window]

        if len(self.requests[key]) >= limit:
            return True

        self.requests[key].append(now)
        return False

    def get_remaining(self, key: str, limit: int = None) -> int:
        limit = limit or settings.RATE_LIMIT_PER_MINUTE
        now = time.time()
        window = 60
        self.requests[key] = [t for t in self.requests[key] if now - t < window]
        return max(0, limit - len(self.requests[key]))


rate_limiter = RateLimiter()
