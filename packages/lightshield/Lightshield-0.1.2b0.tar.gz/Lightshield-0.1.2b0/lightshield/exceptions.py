class LimitBlocked(Exception):
    """Local API blocked Exception that returns a retry_after value in seconds."""
    def __init__(self, retry_after=1):
        self.retry_after = int(retry_after) / 1000
