from rest_framework import serializers
from .models import Cart, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # read_only_fields = ['slug', 'created_at']

class DetailedProductSerializer(serializers.ModelSerializer):
    similar_products = serializers.SerializerMethodField()
    class Meta:
        model = Product
        # fields = '__all__'
        # read_only_fields = ['id', 'name', 'price','slug', 'image', 'description', 'created_at', 'updated_at', 'similar_products']
        fields = ['id', 'name', 'price','slug', 'image', 'description', 'created_at', 'updated_at', 'similar_products']

    def get_similar_products(self, product):
        # Assuming you have a method to get similar products
        products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]
        return ProductSerializer(products, many=True).data
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['cart_code', 'created_at', 'updated_at', 'paid', 'user', 'product', 'quantity']
        # read_only_fields = ['cart_code', 'created_at', 'updated_at', 'paid']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ['id','cart', 'product', 'quantity']

class SimpleCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'num_of_items']

        def get_num_of_items(self, cart):
            num_of_items = sum([item.quantity for item in cart.items.all()])
            return num_of_items
