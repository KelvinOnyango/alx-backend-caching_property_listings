from django.core.cache import cache
from .models import Property

def get_all_properties():
    properties = cache.get('all_properties')
    if not properties:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties

def get_redis_cache_metrics():
    from django_redis import get_redis_connection
    redis = get_redis_connection("default")
    info = redis.info()
    
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0
    
    metrics = {
        'hits': hits,
        'misses': misses,
        'hit_ratio': hit_ratio,
        'total_commands': info.get('total_commands_processed', 0),
        'memory_used': info.get('used_memory', 0),
    }
    
    # Log metrics (configure your logger as needed)
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Redis Cache Metrics: {metrics}")
    
    return metrics