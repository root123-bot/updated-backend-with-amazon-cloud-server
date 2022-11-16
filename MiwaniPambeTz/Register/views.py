from django.shortcuts import render
from django.contrib.auth import get_user_model
from MiwaniPambeTz.Register.serializers import RegistrationSerializer, EmailSerializer, ResetPasswordSerializer  #, ResetPasswordEmailRequestSerializer
from MiwaniPambeTz.Customer.models import Profile
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


class CreateUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        password = request.data['password']
        email = request.data.get('email', None)
        print('This is posted email for you' + str(email))
        print('This is password posted, ' + password)
        try:
            if password:
                password_hash = make_password(password)
                print('This is password hash')
                print(password_hash)
                user = get_user_model().objects.create(email=request.data['email'], password=password_hash)
                profile = Profile.objects.create(user=user)
                user.save()
                serializer = RegistrationSerializer(user)
                return Response(serializer.data)

            return Response({"error": 'Sorry password field should not be empty'}) # , status=status.HTTP_400_BAD_REQUEST
        
        except Exception as err:
            return Response({'err': str(err)})
class ChangePasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data['id']
        password = request.data.get('password', None)
        oldPassword = request.data.get('old', None)

        user = get_user_model().objects.get(id=user_id)

        if password and oldPassword:
            print('Im inside to check this...')
            print(oldPassword, password)
            if user.check_password(oldPassword):  # check password return true if password exist and not otherwise... https://stackoverflow.com/questions/16700968/check-existing-password-and-reset-password
                print('I verified it to true')
                password_hash = make_password(password)
                user.password=password_hash
                user.save()

                # seriailize = RegistrationSerializer(user)
                return Response({"message": "Everything is good, password has been changed.."})
        
        
        return Response({"error": "Sorry password field should not be empty"}) 
        
class PasswordReset(generics.GenericAPIView):
    serializer_class = EmailSerializer

    # Lets override the post method of generic view
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        # The advantage of using .filter() is that it does not throw an error when the
        # query does not exitst instead it return empty array but on using .get() this
        # will throw an error when query is invalid.. So I pick .filter() instead of .get
        # here so as to avoid this kind of things... And when you access [] empty qs array
        # for given index it return 'Blank'...
        user = get_user_model().objects.filter(email=email).first()

        if user:
            # To generate the reset password link we should encode the user want to reset
            # the token and set it in url together with its token.. This is important bcoz
            # this user_id will be used to verify if the one trying to reset is of that user
            # also other important things is token this token is encoded to expire or become
            # invalid if its already been used... Also urlsafe_encode() helps us to safely 
            # transfer the token and encoded user in url for receiver to receive it and perform
            # some logics ...Give credits to this guy https://www.youtube.com/watch?v=zLn7ftlJ_RU&t=24s
            # and https://www.youtube.com/watch?v=mGPerL0RFZA&t=14s
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            
            token = PasswordResetTokenGenerator().make_token(user)

            reset_url = reverse(
                "reset-password", kwargs={'encoded_pk': encoded_pk, 'token': token}
            )


            reset_url = f"localhost:8000{reset_url}"

            # then you should send this url to the user_email.....
            send_mail(
                'Reset Password',
                f'Click this link to reset your password http://localhost:3000/resetConfirm?api={reset_url}',
                settings.EMAIL_HOST_USER,
                [email]
            )
            return Response({
                'message': 'Everything is good see your email for link to reset your password ' + reset_url
            },
                status=status.HTTP_200_OK
            )
        
        else:
            Response({
                'message': 'User does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)
             
class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    # Patch is the request method for CRUD which is the same as UPDATE.. But the patch
    # is partial update https://medium.com/@amattam427/http-patch-method-237f60662652
    # the 'PUT' method will be used if the entire database needs to be updated while 
    # the 'PATCH' method will be used if we're going to do the partial update..
    def patch(self, request, *args, **kwargs):
        # the token and encoded_id is stored in kwargs of request.data, so here we're
        # going to send all kwrags in request.data as kwargs in our context of serializer
        serializer = self.serializer_class(
            data=request.data, context={'kwargs': kwargs}
        )

        serializer.is_valid(raise_exception=True)

        return Response({"message": 'Password reset complete'}, status=status.HTTP_200_OK)

# FROM HERE TESTING THE RESET PASSWORD LOGIC WITH EMAIL BEING SENT TO USER GMAIL...

#password_token = PasswordTokenCheckAPIView.as_view()
change_password = ChangePasswordAPIView.as_view()
create_user = CreateUserAPIView.as_view()