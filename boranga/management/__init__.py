import warnings

from django.core.cache import CacheKeyWarning

# We are not going to use memcached, so we can ignore this warning
warnings.simplefilter("ignore", CacheKeyWarning)
