from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieve all properties from cache or database.
    Cache for 1 hour (3600 seconds).
    """
    cache_key = 'all_properties'
    
    # Try to get data from cache
    cached_properties = cache.get(cache_key)
    
    if cached_properties is not None:
        logger.info("Cache hit for all_properties")
        return cached_properties
    
    # If not in cache, fetch from database
    logger.info("Cache miss for all_properties, fetching from database")
    properties = list(Property.objects.all().select_related())
    
    # Cache the queryset for 1 hour
    cache.set(cache_key, properties, 3600)
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including hit ratio.
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis info
        info = redis_conn.info()
        
        # Extract cache statistics
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_commands = info.get('total_commands_processed', 0)
        connected_clients = info.get('connected_clients', 0)
        used_memory = info.get('used_memory_human', '0B')
        
        # Calculate hit ratio
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0
        
        # Prepare metrics dictionary
        metrics = {
            'hits': hits,
            'misses': misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 4),
            'hit_percentage': round(hit_ratio * 100, 2),
            'total_commands': total_commands,
            'connected_clients': connected_clients,
            'used_memory': used_memory,
        }
        
        # Log metrics
        logger.info(f"Cache Metrics - Hits: {hits}, Misses: {misses}, "
                   f"Hit Ratio: {hit_ratio:.2%}, Total Commands: {total_commands}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0,
            'hit_percentage': 0,
        }
