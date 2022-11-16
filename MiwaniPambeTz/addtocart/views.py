from MiwaniPambeTz.addtocart.serializers import ProductSerializer, CartSerializer, CartProductSerializer, OrderSerializer
from MiwaniPambeTz.Customer.serializers import ProfileSerializer
from rest_framework import generics
from MiwaniPambeTz.addtocart.models import Product, CartProduct, Cart, Order
from MiwaniPambeTz.Customer.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from datetime import datetime, timezone
from django.db.models import Q
import numpy as np
import string, random

class ListAllOrderAPIView(generics.ListAPIView):
    queryset = Order.objects.all().filter(isCompleted=False)
    serializer_class = OrderSerializer

class ListAllProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
 
class AccessGivenProductAPIView(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data['product']
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        print('ALREADY FETCHED IM RETURNING SOMETHING...')
        return Response(serializer.data)


# HII VIEW INAKUA EXECUTED ONLY WHEN USER WANT TO CREATE A CART BUT NOT TO UPDATE THE
# CART...
class CreateCartAPIView(APIView):
    
    # Hii get_queryset ni method yangu mwenyewe hamna iliyokuwepo eti nime-override
    # Hapana nimechek documentation there is no method of get_queryset from APIView or View

    def get_queryset(APIView):
        carts = Cart.objects.all()
        return carts
    
    def get(self, request, *args, **kwargs):
        carts = self.get_queryset()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    
    def post(self, request, *args, **kwargs):
        data = request.data
 
        user_id = request.data.pop('id')
        product_id = request.data.pop('productId')
        product = Product.objects.get(id=product_id)

        user = get_user_model().objects.get(id=user_id)
        subtotal = request.data.pop('price')
        
        print('eti hapa ndo kuna error????')
        new_cart = Cart.objects.create(customer=user, total=subtotal)
        new_cart.save()

        quantity = request.data.pop('quantity')
        # we can have none in customization so lets check if no the return none
        # vilevile property value inaweza ikawa haipo so sio case
        customization = request.data.pop('customization', None)
        propertyValue = request.data.pop('value', None)
        secondPropertyValue = request.data['secondValue']

        new_cartProduct = CartProduct.objects.create(
            cart=new_cart,
            product=product,
            quantity = quantity,
            subTotal = subtotal,
            customization = customization,
            selectedPropertyValue=propertyValue,
            selectedSecondPropertyValue=secondPropertyValue

        )

        new_cartProduct.save()
        
        serializer = CartProductSerializer(new_cartProduct)
        return Response(serializer.data)

class IncreaseCartProductAPIView(APIView):
    def post(self, request, *args, **kwargs):
        cproduct_id = request.data['cpid']
        cp = CartProduct.objects.get(id=cproduct_id)
        cp.quantity = cp.quantity + 1
        cp.subTotal = cp.subTotal + cp.product.price
        cp.save()

        user = get_user_model().objects.get(id=request.data['user_id'])
        cart = Cart.objects.filter(isOrdered=False).get(customer=user)

        qs = cart.cartproduct_set.all()
        total = 0
        for p in qs:
            total = p.subTotal + total

        cart.total = total
        cart.save()

        cp_qs = cart.cartproduct_set.all()
        serialize = CartProductSerializer(cp_qs, many=True)
        return Response(serialize.data)


class DecreaseCartProductAPIView(APIView):
    def post(self, request, *args, **kwargs):
        cproduct_id = request.data['cpid']
        cp = CartProduct.objects.get(id=cproduct_id)
        cp.quantity = cp.quantity  - 1
        cp.subTotal = cp.subTotal - cp.product.price
        cp.save()

        user = get_user_model().objects.get(id=request.data['user_id'])
        cart = Cart.objects.filter(isOrdered=False).get(customer=user)

        qs = cart.cartproduct_set.all()
        total = 0
        for p in qs:
            total = p.subTotal + total

        cart.total = total
        cart.save()

        cp_qs = cart.cartproduct_set.all()
        serialize = CartProductSerializer(cp_qs, many=True)
        return Response(serialize.data)

class RemoveCartProductAPIView(APIView):
    def post(self, request, *args, **kwargs):
        cproduct_id = request.data['cpid']
        cp = CartProduct.objects.get(id=cproduct_id)
        cp.delete()

        user = get_user_model().objects.get(id=request.data['user_id'])
        cart = Cart.objects.filter(isOrdered=False).get(customer=user)

        qs = cart.cartproduct_set.all()
        total = 0
        for p in qs:
            total = p.subTotal + total

        cart.total = total
        cart.save()

        cp_qs = cart.cartproduct_set.all()
        serialize = CartProductSerializer(cp_qs, many=True)

        return Response(serialize.data)


class FilterProductsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data['search']

        ids = []
        qs = query.split()
        # For future hii qs naweza nika-ifilter itoe maneno kama 'of, the, na, kwa, in, ya' and etc coz hazima maana on searching..
        qs = np.unique(qs).tolist()
        # then ukishaifanya iwe unique inabidi ... ndo u-remove but before remove make sure if its included...
        toTrimm = ['kwa',
                    'was',
                    'were',
                    'of',
                    'to',
                    'in',
                    'ya',
                    'from',
                    'is',
                    'na',
                    'and',
                    'pia',
                    'the',
                    'so',
                    'or',
                    'for',
                    'a',
                    'an',
                    'that',
                    'those',
                    'this',
                    'me',
                    'all',
                    'or',
                    'then',
                    'thus',
                    'too',
                    'but',
                    'also',
                    'so',
                    'yet',
                    'too',
                    'for',
                    'another',
                    'hence',
                    'last',
                    'further',
                    'however',
                    'fact',
                    'end',
                    'meanwhite'
        ]
        
        for word in toTrimm:
            if word in qs:
                qs.remove(word)

        
        print('This qs after split')
        print(qs)
        for que in qs:
            products = Product.objects.filter(Q(title__icontains=que) | Q(description__icontains=que) | Q(category__icontains=que) | Q(gender__icontains=que))
            # https://www.codegrepper.com/code-examples/python/django+get+id+from+queryset
            ids_qs = products.values_list('pk', flat=True)
            ids_arr = [i for i in ids_qs]
            ids = ids + ids_arr

        # After that then it means we have all ids of matching query inside our ids array
        # https://www.guru99.com/python-howto-remove-duplicates.html
        unique_ids = np.unique(ids).tolist()
        print('These are state of ids b4 and after')
        print(ids, unique_ids)

        # To fetch or return the qs by using id or any field you want in list/array...
        # then use '__in' keyword....
        # https://stackoverflow.com/questions/56642118/django-filtering-from-a-list-of-ids
        products = Product.objects.filter(id__in=unique_ids)



        # Kwenye searching our priority is to search through
        # product title and then description...
        # products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query) | Q(gender__icontains=query))

        serialize = ProductSerializer(products, many=True);

        return Response(serialize.data)

class CartProductsByThisUserAPIView(APIView):
    # Hii inabidi ipokee post tu... And then i-serialize output in return
    def post(self, request, *args, **kwargs):
        user_id = request.data.pop('id')
        # Nikipata cart itakua rahisi ku-access cartproducts
        user = get_user_model().objects.get(id=user_id)
        try:
            cartByThatUser = Cart.objects.filter(isOrdered=False).get(customer=user)
            # if this succeed then there is a cartByThatUser...
        except Exception as err:
            # then there is no cart by this user
            return Response({"message": "No cart by this user", "code": str(err)})
        
        # so we have cart by that user then what next is to query the all cartproducts
        cp_qs = cartByThatUser.cartproduct_set.all()
        serialize = CartProductSerializer(cp_qs, many=True)

        return Response(serialize.data)

class IsCartExistOrNotAPIView(APIView):

    # In [6]: products = Product.objects.all().get(id=4)

    def post(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        user = get_user_model().objects.get(id=user_id)

        try:
            cartByThatUser = Cart.objects.filter(isOrdered=False).get(customer=user)

            cartproducts_qs = cartByThatUser.cartproduct_set.all()
            cp = [x for x in cartproducts_qs if x.product.id == int(request.data['productId'])]

            if len(cp) > 0:
                # then cartproduct by this id is already exist in the cart...

                # Lets now check if the customization of that cp in the cart is the same as the incoming one

                imepatikana = False
                ind = 0
                print('HEY THIS IS CP FOR YOU INABIDI IRETURN MBILI INSTEAD OF ONE')
                print(cp)
                for c in cp:  # Humu zinaweza zikawa cp product nyingi zenye different customizations
                    print('THIS WHAT YOU WANT THIS WHAT YOU GET..')
                    print(c.customization, request.data['customization'], c.selectedPropertyValue, request.data['value'], c.selectedSecondPropertyValue, request.data['secondValue'])
                    if c.customization == request.data['customization'] and c.selectedPropertyValue == request.data['value'] and c.selectedSecondPropertyValue == request.data['secondValue']:
                        print('NIMEPATIKANA')
                        imepatikana = True
                        ind = cp.index(c)
                        break
                print('Imepatikana au la')
                print(imepatikana, ind)
                if imepatikana == False:
                    # then we need to create a new cartproduct
                    print('Haijapatikana')
                    product = Product.objects.get(id = int(request.data['productId']))
                    quantity = request.data['quantity']
                    subtotal = request.data['price']
                    customization = request.data['customization']
                    propertyValue = request.data['value']
                    secondPropertyValue = request.data['secondValue']
                    print(secondPropertyValue)
                    new_cartProduct = CartProduct.objects.create(
                        cart=cartByThatUser,
                        product=product,
                        quantity = quantity,
                        subTotal = subtotal,
                        customization = customization,
                        selectedPropertyValue=propertyValue,
                        selectedSecondPropertyValue=secondPropertyValue
                    )

                    new_cartProduct.save()

                    qs = cartByThatUser.cartproduct_set.all()
                    total = 0
                    for p in qs:
                        total = p.subTotal + total

                    print('Im updating the total of the cart..')
                    # Au hii ina create a new cart instead of update it...
                    cartByThatUser.total = total
                    cartByThatUser.save()

                else:
                    # then we have already the same cart...
                    cp[ind].quantity = cp[ind].quantity + request.data['quantity']
                    cp[ind].subTotal = cp[ind].product.price * cp[ind].quantity

                    print('This is the updated cartproduct')
                    print(cp[ind])
                    cp[ind].save()

                    qs = cartByThatUser.cartproduct_set.all()
                    total = 0
                    for p in qs:
                        total = p.subTotal + total

                    cartByThatUser.total = total
                    cartByThatUser.save()
            
            else:
                product = Product.objects.get(id = int(request.data['productId']))
                quantity = request.data['quantity']
                subtotal = request.data['price']
                customization = request.data['customization']
                propertyValue = request.data['value']
                secondPropertyValue = request.data['secondValue']

                # then that's a new cartproduct you should create a new cartproduct..
                new_cartProduct = CartProduct.objects.create(
                    cart=cartByThatUser,
                    product=product,
                    quantity = quantity,
                    subTotal = subtotal,
                    customization = customization,
                    selectedPropertyValue=propertyValue,
                    selectedSecondPropertyValue=secondPropertyValue

                )

                new_cartProduct.save()

                qs = cartByThatUser.cartproduct_set.all()
                total = 0
                for p in qs:
                    total = p.subTotal + total

                cartByThatUser.total = total
                cartByThatUser.save()
            
            return Response({"status": True, "cart": cartByThatUser.id})
        
        except Exception as e:
            print('Kuna error nahisi hii ndo inafanya new cart inakua created...')
            return Response({"status": False, "err": str(e)})


class ProductOfGivenCategoryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        category = request.data['category']
        p_qs = Product.objects.filter(category=category)
        serialize = ProductSerializer(p_qs, many=True)
        return Response(serialize.data)


class ProductOfGivenGenderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        gender = request.data['gender']
        p_qs = Product.objects.filter(gender=gender)
        serialize = ProductSerializer(p_qs, many=True)
        return Response(serialize.data)


class ViewProfileAPIView(APIView):
    # Hii kazi yake ni kutumia kule profile info..
    # Here you should post to us the id of the user
    # in order for you to access profile
    # Nahisi on creating user we should also create a profile for them..
    
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data['id']
            user = get_user_model().objects.get(id=user_id)
            
            profile = Profile.objects.get(user=user)

            serialize = ProfileSerializer(profile)

            return Response(serialize.data)
        except:
            return Response({'error': 'No profile by that user...'})


class EditProfileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data['id']
        img = request.data.get("image", None)
        name = request.data.get("name", None)

        
        
        user = get_user_model().objects.get(id=user_id)
        profile = Profile.objects.get(user=user)

        if name:
            profile.full_name = name
            profile.save()
        
        if img and img != 'null':
            
            profile.profile_picture = img
            profile.save()
        
        serialize = ProfileSerializer(profile)
        return Response(serialize.data)

        
class CreateOrderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        cart_id = request.data['cartId']
        user_id = request.data['id']
        phone = request.data['mobile']
        order_id = request.data['transactionId']
        
        # Haziwezi zikafanana id coz hapa hatuquery cart by user but tuna-query cart by id ko no
        # means of un-ordered and ordered cart to be the same...
        cart = Cart.objects.get(id=cart_id)
        cart.isOrdered = True
        cart.save()
        user = get_user_model().objects.get(id=user_id)
        unique_id = "".join(random.choices(string.ascii_uppercase + string.digits, k = 30))
        order = Order.objects.create(
            cart = cart,
            ordered_by = user,
            mobile = phone,
            orderId = order_id,
            uniqueOrderId = unique_id
        )

        order.save()
        return Response({"success": "Your order has been created successful", 'unique_id': unique_id, 'phone': phone, 'orderId': order_id })


class ClearCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # I need the cart_id to be passed if not then use the user id
        # by using the user id we can detect which cart that is un-ordered
        # by that user..
        # we expect the user_id to be passed..
        user_id = request.data['user_id'];
        user = get_user_model().objects.get(id=user_id)
        cartByThatUser = Cart.objects.filter(isOrdered=False).get(customer=user)
        cartByThatUser.cartproduct_set.all().delete();
        return Response({'message': 'Cart has been cleared....'})


allOrders = ListAllOrderAPIView.as_view()
clear_cart = ClearCartAPIView.as_view()
product_metadata = AccessGivenProductAPIView.as_view()
create_order = CreateOrderAPIView.as_view()
edit_profile = EditProfileAPIView.as_view()
profile = ViewProfileAPIView.as_view()
output = FilterProductsAPIView.as_view()
p_gender = ProductOfGivenGenderAPIView.as_view()
products = ProductOfGivenCategoryAPIView.as_view()
cp_remove = RemoveCartProductAPIView.as_view()
cp_increase = IncreaseCartProductAPIView.as_view()
cp_decrease = DecreaseCartProductAPIView.as_view()
cart_products_by_user = CartProductsByThisUserAPIView.as_view()
check_cart_by_user = IsCartExistOrNotAPIView.as_view()    
cart_list_view = CreateCartAPIView.as_view()
product_list_view = ListAllProductAPIView.as_view()
