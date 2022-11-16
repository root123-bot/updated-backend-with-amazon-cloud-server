from django.shortcuts import render
from MiwaniPambeTz.Register.forms import CustomUserCreationForm
from django.views.generic import View
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
class RegistrationView(View):
    template_name='registration/signup.html'
    user_form = CustomUserCreationForm
    success_url = 'https://www.google.com'

    def get(self, request):
        return render(request, self.template_name, {'form': self.user_form})

    def post(self, request):
        user_bound_form = self.user_form(request.POST)
        

            # HII INASUMBUA COZ UNAKUWA HUJAWEKA STRONG PASSWORD BUT SIJAELEWA HIZI MAMBO ZA STRONG PASSWORD ZINATOKA WAPI WAKATI MIMI VALIDATIONS ZANGU
            # HIZO HAPO JUU HIZO ZA STRONG PASSWORD SIJAWEKA AU ZINAKUWA INHERITED FROM 'USERCREATIONFORM' KAMA NDO HIVYO MAKE SURE UNA-ZIOVERRIDE MAPEMA KABISA 
            # COZ HII ITAKUJA KUSUMBUA....... OK NISHAPATA JIBU NI KWA NINI ISHU KAMA HII INATOKEA NI KWA SABABU IN settings.py there is 'AUTH_PASSWORD_VALIDATORS' which
            # add strong password validation to on creating password... Ko hata kama validation za form hapa zime-pass kama hizi zilizopo kwenye hii AUTH_PASSWORD_VALIDATIONS
            # hazijapass ujue kazi ipo lazima itakataa ku-create huyo user....Ko ukiangalia hii variable inakwambia kuwa 'Name of user should not be the same to
            # password, then kuna ishu ya MinimumLengthValidator, CommonPasswordValidator, and NumericPasswordValidator ukiangalia source code zake utajua inakuaje
            # but kama huzitaki then delete them in this variable of AUTH_PASSWORD_VALIDATORS... Ko nahisi hadi hapo ushaelewa kuwa validation zipo nying sio tu hizi ulizonazo
            # hapa in this form.... this is from Register/forms.py
        if user_bound_form.is_valid():
            print('The form is valid... NO NEED TO WORRY ')
            user = user_bound_form.save()
            group = Group.objects.get(name="Customer")
            user.groups.add(group)
            messages.success(request, 'Your account has been created successful')
            return redirect(self.success_url)
        else:
            print('Your form is invalid')
            
            return render(request, self.template_name, {'form': self.user_form})