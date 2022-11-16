from django.conf.urls import url
from .views import UserLogin

urlpatterns = [
    url(r'login/$', UserLogin.as_view(), name='login')
]