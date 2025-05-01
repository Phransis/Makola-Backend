from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view(['GET'])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    
@api_view(['GET'])
def products_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

@api_view(['GET'])
def product_category(request, category_slug):
    products = Product.objects.filter(category__slug=category_slug)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
