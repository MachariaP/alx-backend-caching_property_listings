from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

@receiver([post_save, post_delete], sender=Property)
def invalidate_property_cache(sender, **kwargs):
    """
    Invalidate the all_properties cache when a Property is created, updated, or deleted.
    """
    cache_key = 'all_properties'
    if cache.delete(cache_key):
        logger.info(f"Cache invalidated for {cache_key} due to {sender.__name__} {kwargs.get('created', 'update/delete')}")
    else:
        logger.info(f"Cache key {cache_key} not found or already invalidated")
