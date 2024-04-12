HIGHEST_PRIORITY = 0
HIGH_PRIORITY = 100
DEFAULT_PRIORITY = 1000


class Ordered:
    def get_priority(self):
        """Higher is better."""
        raise NotImplementedError()
