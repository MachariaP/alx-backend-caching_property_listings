from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse
from .utils import get_redis_cache_metrics

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/property_list.html', {'properties': properties})

def cache_metrics(request):
    """
    View to display Redis cache metrics.
    """
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)
