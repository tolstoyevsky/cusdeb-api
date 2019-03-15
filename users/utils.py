"""Module containing utils for the CusDeb API Users application. """

from functools import wraps

from django.http import Http404
from social_core.exceptions import MissingBackend
from social_django.compat import reverse
from social_django.utils import load_backend, load_strategy as base_load_strategy


def psa(redirect_uri=None, load_strategy=base_load_strategy):
    """Python-social-auth. """
    def decorator(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = reverse(redirect_uri, args=(kwargs.pop('version'), backend,))
            request.social_strategy = load_strategy(request)
            # backward compatibility in attribute name, only if not already
            # defined
            if not hasattr(request, 'strategy'):
                request.strategy = request.social_strategy

            try:
                request.backend = load_backend(request.social_strategy,
                                               backend, uri)
            except MissingBackend:
                raise Http404('Backend not found')
            return func(request, backend, *args, **kwargs)
        return wrapper
    return decorator
