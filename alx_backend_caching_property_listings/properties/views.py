from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property
from .utils import get_all_properties
from .serializers import PropertySerializer

@cache_page(60 * 15)  # Cache for 15 minutes
@api_view(['GET'])
def property_list(request):
    properties = get_all_properties()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)