from django.contrib import admin
from .models import Order, Product, Cart, CartProduct, Image, SecondPropsSelection


class CustomOrder(admin.ModelAdmin):
    list_display = ('uniqueOrderId', 'orderId', 'mobile',
                    'cart', 'isCompleted', 'create_at')
    date_hierarchy = 'create_at'
    list_filter = ('create_at', 'isCompleted')
    search_fields = ('uniqueOrderId', 'mobile', 'orderId',)

    # Kama fields huwezi uka-change au ku-edit usiiweke hapa
    # hapa kwenye field sets inabidi zikae fields ambazo wewe kama
    # admin unaweza ukaedit mfano is_ordered and so on..
    fieldsets = (

        ('Order status', {
            'fields': [
                'isCompleted',
            ],
        }),
    )


class CustomCart(admin.ModelAdmin):
    list_display = ('customer', 'total', 'created_at', 'isOrdered')
    date_hierarchy = 'created_at'
    list_filter = ('created_at', 'isOrdered')
    search_fields = ('customer', )

    # Kama fields huwezi uka-change au ku-edit usiiweke hapa
    # hapa kwenye field sets inabidi zikae fields ambazo wewe kama
    # admin unaweza ukaedit mfano is_ordered and so on..
    fieldsets = (

        ('Order status', {
            'fields': [
                'isOrdered',
            ],
        }),
    )

class CustomCartProduct(admin.ModelAdmin):
    list_display = ('cart', 'quantity', 'subTotal', 'product', 'selectedPropertyValue', 'selectedSecondPropertyValue', 'customization', 'date_added')
    date_hierarchy = 'date_added'
    list_filter = ('date_added', )
    

    fieldsets = (
        ('Don\'t Change', {
            'fields': [
              'customization',
            ],
        }),
    )


class CustomProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'gender', 'category', 'added_date')
    date_hierarchy = 'added_date'
    list_filter = ('added_date', )
    search_fields = ('title', 'description')


# Register your models here.
admin.site.register(Product, CustomProduct)
admin.site.register(Order, CustomOrder)
admin.site.register(Cart, CustomCart)
admin.site.register(CartProduct, CustomCartProduct)
admin.site.register(Image)
admin.site.register(SecondPropsSelection)
