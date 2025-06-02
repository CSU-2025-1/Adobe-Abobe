FILTER_REGISTRY = {}


def register_filter(name):
    def decorator(fn):
        FILTER_REGISTRY[name] = fn
        return fn

    return decorator
