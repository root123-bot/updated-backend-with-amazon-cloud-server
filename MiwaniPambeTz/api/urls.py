from django.conf.urls import url
from MiwaniPambeTz.Register.views import create_user, change_password, PasswordReset, ResetPassword
from MiwaniPambeTz.addtocart.views import (
    product_list_view,
    cart_list_view, 
    check_cart_by_user, 
    cart_products_by_user,
    cp_increase, 
    cp_decrease,
    cp_remove,
    products,
    p_gender,
    output,
    profile,
    edit_profile,
    create_order,
    product_metadata,
    clear_cart,
    allOrders
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)

from django.urls import path


urlpatterns = [
    path("placed_orders/", allOrders, name='orders'),
    path("password-reset/", PasswordReset.as_view(), name='reset'),
    path("password-reset/<str:encoded_pk>/<str:token>/", ResetPassword.as_view(), name='reset-password'),  # Hii baadae tutaibadilisha...
    url(r'flash_cart', clear_cart, name="clear_cart"),
    url(r'product/$', product_metadata, name='product'),
    url(r'create_order/$', create_order, name='create_order'),
    url(r'change_password/$', change_password, name='change_password'),
    url(r'edit/$', edit_profile, name='edit_profile'),
    url(r'profile/$', profile, name='profile'),
    url(r'output/$', output, name='result_of_search'),
    url(r'products_by_gender/$', p_gender, name='productOfGivenGender'),
    url(r'products_by_category/$', products, name='productOfGivenCategory'),
    url(r'cp_remove/$', cp_remove, name='delete_cp'),
    url(r'cp_increase/$', cp_increase, name='increase_cp'),
    url(r'cp_decrease/$', cp_decrease, name="increase_cp"),
    url(r'cartproducts/$', cart_products_by_user, name='givenUser_cps'),
    url(r'cartExistOrNot/$', check_cart_by_user, name='check_cart'),
    url(r'carts/$', cart_list_view, name='allCarts'),
    url(r'products/$', product_list_view, name='allProducts'),
    url(r'register/$', create_user, name='register'),
    url(r'token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]