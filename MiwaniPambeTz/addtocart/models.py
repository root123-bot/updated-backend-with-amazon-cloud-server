from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

# so in this image first you will put the characterType like color, material and so on then 
# down below in characterValue you will put the value of that character example if you've 
# selected 'color' in characterType then in characterVAlue you put value of the 'color' which 
# maybe its a 'Black'

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Unisex', 'Unisex'),
)

CATEGORY_CHOICES = (
    ('Watch & Bracelets', 'Watch & Bracelets'),
    ('Necklace/Chain', 'Necklace/Chain'),
    ('Glass', 'Glass'),
    ('Ring', 'Ring'),
    ('T-Shirt', 'T-Shirt'),
    ('Other', 'Other')
)

DELIVERY_CHOICES = (
    ("Pick at station", "Pick at station"),
    ("Door step pickup", "Door step pickup")
)

ORDER_STATUS = (
    ("Working on it", "Working on it"),
    ("Completed", "Completed")
)

class Image(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    characterType = models.CharField(max_length=200, null=True, blank=True)
    characterValue = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.characterType}: {self.characterValue}'


class SecondPropsSelection(models.Model):
    propType = models.CharField(max_length=200)
    propValue = models.CharField(max_length=200)


    def __str__(self):
        return f'{self.propType} | {self.propValue}'

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField()
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    added_date = models.DateTimeField(auto_now_add=True)
    isInStock = models.BooleanField(default=True)
    images = models.ManyToManyField(Image)
    secProps = models.ManyToManyField(SecondPropsSelection, blank=True, null=True)
    isCustomized = models.BooleanField(default=False)
    hasPropertySelection = models.BooleanField(default=False)
    hasSecondPropertySelection = models.BooleanField(default=False)
    amountInStock = models.PositiveIntegerField(default=100)

    @property
    def get_urls(self):
        images_urls = []
        for image in self.images.all(): 
            # ManyRelatedManager obj is not related...
            if(image.photo): 
                url = image.photo.url # Kaka hii ni image field unachokifanya wewe ni kustore image humu badala ya path tu...
                print(url)
                images_urls.append(url)

        
        # HAPA INABIDI UJUE NI KWA NINI KUNA PROPERTY METHOD IN MODEL MAY BE WANATAKA URETURN KITU KILICHOPO KWENYE MODEL
        return images_urls
    
    @property
    def map_secondProps(self):
        if self.hasSecondPropertySelection:
            property_value = []

            for prop in self.secProps.all():
                property_value.append({prop.propType: prop.propValue})
            
            return property_value

        return {'message': 'There is no second property selection in this product.'}
    

    @property
    def second_propsValue(self):
        if self.hasSecondPropertySelection:
            values = []
            
            for prop in self.secProps.all():
                values.append(prop.propValue)
            
            return values
        
        return []
    
    @property
    def map_property(self):
        if self.hasPropertySelection:
            property_value = []
            
            for image in self.images.all():
                property_value.append({image.characterType: image.characterValue})
                

            return property_value
        
        return {'message': 'There is no property selection in this product'}

    @property
    def property_values(self):
        if self.hasPropertySelection:
            values = []

            for image in self.images.all():
                values.append(image.characterValue)
            
            return values
        
        return []

    def __str__(self):
        return self.title

# Hii hasPropertySelection ni kwamba itatumika kutuambia kama hiyo product user anaweza
# akachagua property fulani and on Frontend if the Product hasPropertySelection we'll go
# to the images(models.ManyToManyField(Images)) and read on the Property field of the
# Image and we'll include it in the interface then the user will read that and select it in
# the radio buttons, in case there is no selection then the first Image property will be used
# as the selected one.... Also we should update the CartProduct to accept the value selected...
# ok ndo hii maanake
  



# one user is associated with one cart
class Cart(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    isOrdered = models.BooleanField(default=False)
    mode = models.CharField(max_length=100, choices = DELIVERY_CHOICES, default='Pick at station')

    def __str__(self):
        return f'Customer email: {self.customer.email}'

    

# if the product selected by the user isCustomized is True then will will allow the
# user to add his customizations if its not customized then there'll be no a box/textarea
# to add customization... Also the customization field can be blank or null because sometimes
# user has no need to add any customization ...
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    subTotal = models.PositiveIntegerField()
    customization = models.TextField(blank=True, null=True)
    selectedPropertyValue = models.CharField(max_length=200, null=True, blank=True)
    selectedSecondPropertyValue = models.CharField(max_length=200, blank=True, null=True)

    @property
    def get_urls(self):
        images_urls = []
        for image in self.product.images.all():
            if(image.photo):
                url = image.photo.url
                print(url)
                images_urls.append(url)
        
        return images_urls
    
    @property
    def get_cartId(self):
        return self.cart.id
    
    @property
    def get_title(self):
        return self.product.title

    @property
    def get_prop(self):
        print('im going to check')
        if self.product.hasPropertySelection:
            print('im insider')
            for image in self.product.images.all():
                if len(image.characterType) != 0:
                    print('something is here')
                    # then we have prop selection here..
                    print('Im inside if statement')
                    return image.characterType 

        return "NONE"

    @property
    def get_secondProp(self):
        if self.product.hasSecondPropertySelection:
            for prop in self.product.secProps.all():
                # our aim is to get propType..
                if len(prop.propType) != 0:
                    return prop.propType
        
        return "NONE"

    def __str__(self):
        return f"{self.product.title}: Tsh {self.subTotal}"
# selectedPropertyaValue will contain the value of the property like color and so on to 
# enable to store the value of property selected by the user and this get tracked in the
# Product where admin or person who post the product he should tell us if the product has 
# given property if so then this selectedPropertyValue field should contain the given value...


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, blank=True, null=True)
    ordered_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.CharField(max_length=500, null=True, blank=True)
    mobile = models.CharField(max_length=500)
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS, default='Working on it')
    create_at = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=200, null=True, blank=True)
    ward = models.CharField(max_length=200, null=True, blank=True)
    orderId = models.CharField(max_length=200)  # Hapa ndo ataweka namba ya muamala
    isCompleted = models.BooleanField(default=False)   # HII FIELD NI MUHIMU IJAZWE PALE ORDER INAPOKUWA TIAR PROCESSED...
    uniqueOrderId = models.CharField(max_length=100, blank=True, null=True)
    # Mwanzo scenario yangu nilikua nataka hii orderId iwe ndo inayotumika kama kitambulisho cha
    # ku-refer orderId ko ni kitu ambacho ni unique but nimegundua kuna user vichaa wanaweza wakawa
    # wanaweka namba za uongo but kwa mfano mtu akiweka namba ya uongo ileile moja mara 3 ko haiwezi
    # ikawa unique for that case we should come with unique orderId instead of depend on vulnerable 
    # orderId powered by user input of transactionId...


    def __str__(self):
        return "Order: "+str(self.id)


    
    