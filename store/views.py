from django.shortcuts import get_list_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
# Create your views here.


@api_view()
def product_list(request):
    queryset = Product.objects.select_related("collection").all()
    serializer = ProductSerializer(
        queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    product = get_list_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    datas = serializer.data
    return Response(datas)


@api_view()
def collection_detail(request, pk):
    return Response("ok")
