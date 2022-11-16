from enum import unique
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, unique=True, related_name='customer')
    full_name = models.CharField(verbose_name='Full name', max_length=200, default='431EFD#')
    profile_picture = models.ImageField(verbose_name='Avatar', upload_to='images', default='images/profile.png')
    is_customer = models.BooleanField(default=True)

    @property
    def get_email(self):
        return self.user.email
    
    def __str__(self):
        return self.full_name   