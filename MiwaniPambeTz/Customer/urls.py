from django.conf.urls import url
from .views import RegistrationView

urlpatterns = [
    url(r'^register/$', RegistrationView.as_view(), name='register')

]