class Action:
    """PipelineManager action representation."""

    def __init__(self, f, priority, cache_name=None):
        self.f = f
        self.priority = priority
        self.cache_name = cache_name

    def __call__(self, *args, **kwargs):
        return self.f(*args, *kwargs)
