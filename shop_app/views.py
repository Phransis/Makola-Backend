from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CartItem, Product
from .serializers import ProductSerializer
import logging

logger = logging.getLogger(__name__)

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
@api_view(['GET'])
def product_in_cart(request):
    cart_code = request.query_params.get('cart_code')
    product_id = request.query_params.get('product_id')
    try:
        cart_item = CartItem.objects.get(cart_code=cart_code)
        product = Product.objects.get(id=product_id)

        product_exists_in_cart = cart_item.product.filter(id=product.id).exists()
        if product_exists_in_cart:
            return Response({"message": "Product is in the cart"}, status=200)
        else:
            return Response({"message": "Product is not in the cart"}, status=404)

    except CartItem.DoesNotExist:
        return Response({"error": "Product not found in cart"}, status=404)

@api_view(['GET'])
def product_in_cart(request, cart_code):
    try:
        cart_items = CartItem.objects.filter(cart__cart_code=cart_code)
        serializer = ProductSerializer(cart_items, many=True)
        return Response(serializer.data)
    except CartItem.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

@api_view(['POST'])
def mytest_view(request):
    institution_id = request.data.get('institution_id')
    institution_action = request.data.get('institution_action')
    institution_name = request.data.get('institution_name')
    institution_email = request.data.get('institution_email')
    korba_pay_id = request.data.get('korba_pay_id')
    ussd_code = request.data.get('ussd_code')
    ussd_type = request.data.get('ussd_type')
    activation_code = request.data.get('activation_code')

    logger.info(f"Response: {institution_id}, {institution_action}, {institution_name}, {institution_email}, {korba_pay_id}, {ussd_code}, {ussd_type}, {activation_code}")  # Logs the response


    # This is a test view to check if the server is running correctly
    return JsonResponse({
        "institution_id": institution_id,
        "institution_action": institution_action,   
        "institution_name": institution_name,
        "institution_email": institution_email,
        "korba_pay_id": korba_pay_id,
        "ussd_code": ussd_code,
        "ussd_type": ussd_type,
        "activation_code": activation_code,
        "message": "Success"}, status=200)
