from rest_framework import serializers
from .models import Product, CartProduct, Cart, Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'mobile',
            'orderId',
            'uniqueOrderId'
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'gender',
            'category',
            'added_date',
            'images',
            'isCustomized',
            'hasPropertySelection',
            'get_urls',
            'map_property',
            'property_values',
            'hasSecondPropertySelection',
            'map_secondProps',
            'second_propsValue',
        ]  

        # Hii 'get_urls' ni fields get mapped from the same name
        # of def get_urls(self) from the property method found in 
        # the Product model and this will gives us all urls of the 
        # image.... 


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = [
            'id',
            'cart', 
            'product', 
            'date_added', 
            'quantity', 
            'subTotal', 
            'customization', 
            'selectedPropertyValue',
            'selectedSecondPropertyValue' ,
            'get_urls', 
            'get_title', 
            'get_prop', 
            'get_secondProp',
            'get_cartId'
        ]
 
# Hii ndo ya ku-serialize coz we want to create a new cart here.... not cartProduct...
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['total', 'created_at']


