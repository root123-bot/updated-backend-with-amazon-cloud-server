from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User

# Create your models here.... NA EMBU NIKWAMBIE ULIKUA ZAMANI UNAJIDANGANYA KUWA METHODS ZOTE ZILIZOPO KWENYE INHERITED CLASS LIKE HERE IN BaseUserManager GET CALLED AUTOMATICALLY
# HUO NI UONGO LAZIMA ILI ZI-EXECUTE ZIWE CALLED KWA MFANO HAPA KWENYE USERMANAGER WE CALLED .normalize_email() so bila kui-call haiwi-executed nahisi umepata picha hapa....
# FOR ANY MEANS THE UserManager() object is required on creating the user by the CreateUser.. the user manager is one who can do some functionality about the system....
class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)  # this normalize_email is found in BaseUserManager class and as we said this class method of normalize email can be called by both class or object..
        # Python pop() method removes an element from the dictionary. It removes the element which is associated to the specified key.
        # If specified key is present in the dictionary, it remove and return its value. 
        # If the specified key is not present, it throws an error KeyError.
        # In our case here pop() we pass default value to be returned instead of ThrowingError, the default value is 'False' so if the element of that key is not found then 
        # it should return 'False' instead of throwing an error.... for more read here https://www.w3schools.com/python/ref_dictionary_pop.asp
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop('is_superuser', False)
        # the .model get supplied from BaseUserManager which is a child of models for more check the source codes of BaseUserManager utaona ni class BaseUserManager(models.Manager); embu mwangalie Manager in
        # django.db.models.manager utaona kuna unknown 'className' anainherit after calling from.queryset found in BaseManager
        user = self.model(email=email, is_active=True, is_staff=is_staff, is_superuser=is_superuser, **kwargs)
        # so the returned 'user' object above will have some properties and attributes like set_password and save
        user.set_password(password)
        # the 'using' keyword allow save() to perform the operation against a database that's not the default value in settings.py.. Its used in case u have multiple database in your project
        # For more read page 298 in Beginning Django web Application development.pdf book
        # user.save(using=self._db) usually defined as "default" from your database configuration in settings.py. Behind the scene self._db set as None. If user.save(using=None), then it will use default database.
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        # the _create_user defined above as functionality for us to use here to create a user
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)  # these is_staff and is_superuser are **kwargs which we specified in _create_user() function above since
        # the is_staff acts as key while True is value and so on so there is a meaning for us to define **kwargs in _create_user() where later they gonna be user and checked either to 
        # create super user or normal user....... either its staff or not staff




class CustomUser(AbstractBaseUser, PermissionsMixin):
    # models is from above, we imported above... 
    email = models.EmailField('email address', max_length=254, unique=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_superuser = models.BooleanField('admin status', default=False)
    joined = models.DateTimeField('Date joined', auto_now_add=True)

    USERNAME_FIELD = 'email'  # we add this to be used in AbstractBaseUser by get_username() method and other methods like clean and so on... we also override __str__() of
    # AbstractBaseUser to return email....

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email


    # other methods concerning the permission like has_perm() and has_module_pers() is inherited from PermissionMixin and since there is no changes to make to them
    # we don't going to define them there..

    objects = UserManager()