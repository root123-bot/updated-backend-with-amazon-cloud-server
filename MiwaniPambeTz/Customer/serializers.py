from rest_framework import serializers
from MiwaniPambeTz.Customer.models import Profile
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = [
            'get_email',
            'full_name',
            'profile_picture'
        ]


