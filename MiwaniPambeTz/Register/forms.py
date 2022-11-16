from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='What\'s your email', required=True)
    password1 = forms.CharField(label='Create a password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm the password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        print('This is email we have')
        print(email)
        print('This is user model currenty')
        print(get_user_model())
        user_count = get_user_model().objects.filter(email=email).count()   # hii get_user_model itakua inashida........

        if user_count > 0:
            print('im inside')
            raise forms.ValidationError('This email has already been registered!')
        return email
    

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.data.get('password2')

        print(str(password1) + "|" + str(password2))

        if password1 != password2:
            print('This is the validation of password im inside...')
            raise forms.ValidationError('Password didn\'t match!')
        
        return password1



# HII INASUMBUA COZ UNAKUWA HUJAWEKA STRONG PASSWORD BUT SIJAELEWA HIZI MAMBO ZA STRONG PASSWORD ZINATOKA WAPI WAKATI MIMI VALIDATIONS ZANGU
# HIZO HAPO JUU HIZO ZA STRONG PASSWORD SIJAWEKA AU ZINAKUWA INHERITED FROM 'USERCREATIONFORM' KAMA NDO HIVYO MAKE SURE UNA-ZIOVERRIDE MAPEMA KABISA 
# COZ HII ITAKUJA KUSUMBUA....... OK NISHAPATA JIBU NI KWA NINI ISHU KAMA HII INATOKEA NI KWA SABABU IN settings.py there is 'AUTH_PASSWORD_VALIDATORS' which
# add strong password validation to on creating password... Ko hata kama validation za form hapa zime-pass kama hizi zilizopo kwenye hii AUTH_PASSWORD_VALIDATIONS
# hazijapass ujue kazi ipo lazima itakataa ku-create huyo user....Ko ukiangalia hii variable inakwambia kuwa 'Name of user should not be the same to
# password, then kuna ishu ya MinimumLengthValidator, CommonPasswordValidator, and NumericPasswordValidator ukiangalia source code zake utajua inakuaje
# but kama huzitaki then delete them in this variable of AUTH_PASSWORD_VALIDATORS... Ko nahisi hadi hapo ushaelewa kuwa validation zipo nying sio tu hizi ulizonazo
# hapa in this form....