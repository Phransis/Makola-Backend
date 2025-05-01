from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CartItem, Product
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

# @api_view(['POST'])
# def add_item(request, product_id):
#     try:
#         product = Product.objects.get(id=product_id)
#         cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
#         if created:
#             return Response({"message": "Product added to cart"}, status=201)
#         else:
#             return Response({"message": "Product already in cart"}, status=200)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found"}, status=404)
    
@api_view(['POST'])
def add_item(request):
    cart_code = request.data.get('cart_code')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    
    try:
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        if created:
            cart_item.quantity = quantity
            cart_item.save()
            return Response({"message": "Product added to cart"}, status=201)
        else:
            cart_item.quantity += quantity
            cart_item.save()
            return Response({"message": "Product quantity updated"}, status=200)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
