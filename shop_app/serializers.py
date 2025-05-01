from rest_framework import serializers
from .models import Product

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