# account/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.forms import SignupForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render


from setup.models import ThemeSettings
try:
    theme_address = ThemeSettings.objects.get().name
except:
    theme_address = 'default'


from django.shortcuts import render, get_object_or_404
from .models import UserProfile


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from allauth.account.views import SignupView, _ajax_response



from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.http import (
    Http404,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateResponseMixin, TemplateView, View
from django.views.generic.edit import FormView

from allauth.exceptions import ImmediateHttpResponse
from allauth.utils import get_form_class, get_request_param
from allauth.account import app_settings, signals
from allauth.account.adapter import get_adapter

from .forms import (
    AddEmailForm,
    ChangePasswordForm,
    LoginForm,
    MyLoginForm,
    MySignupForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SetPasswordForm,
    SignupForm,
    UserTokenForm,
    ProfileForm
)
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from allauth.account.utils import (
    complete_signup,
    get_login_redirect_url,
    get_next_redirect_url,
    logout_on_password_change,
    passthrough_next_redirect_url,
    perform_login,
    sync_user_email_addresses,
    url_str_to_user_pk,
)

from allauth.account.views import RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, CloseableSignupMixin

INTERNAL_RESET_URL_KEY = "set-password"
INTERNAL_RESET_SESSION_KEY = "_password_reset_key"


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("oldpassword", "password", "password1", "password2")
)


class SignUpView(generic.CreateView):
    
    template_name = 'account/signup.html'
    

class Login(LoginView):
    template_name = 'account/login.html'


class Logout(LogoutView):
    template_name = 'account/logged_out.html'


def password_update(request):
    if request.method == 'POST':
            
        try:
            user = UserProfile.objects.get(id=request.session['user_profile_id'])
            password = request.POST['password']
            password_2 = request.POST['password_2']

            if password == password_2:
                user.password = password
                user.save()
                return redirect('account:account_profile')
            else:

                return redirect('account:account_profile')


            
        
        except Exception as e:
            print(e)
            return redirect('home')



def account_password(request):

    try:
        user = UserProfile.objects.get(id=request.session['user_profile_id'])

        context = {

        }
        
        return render(request, 'account/account_password.html', context)
    
    except Exception as e:
        print(e)
        return redirect('home')


def account_password_reset(request):

    try:
        user = UserProfile.objects.get(id=request.session['user_profile_id'])

        password = [random.randint(0, 9) for i in range(4)]

        password = ''.join(map(str, password))
        
        user.password = password
        user.save()

        text = f'Пароль доступа {password}'
        telephone=user.telephone

        send_sms(text, telephone)


        context = {

        }
        
        return redirect('account:account_profile')
    
    except:
        return redirect('home')
    


def my_logout(request):
    try:
        user = UserProfile.objects.get(id=request.session['user_profile_id'])
        del request.session['user_profile_id']
        return redirect('home')
    except:
        return redirect('home')
        


def my_login(request):

    form = MyLoginForm()
    if request.method == 'POST':


        form = MyLoginForm(request.POST)
        if form.is_valid():
            user_phone = request.POST['telephone']
            password = request.POST['password']
            

            try:
                userprofile = UserProfile.objects.get(telephone=user_phone)
                if userprofile.password == password:
                    
                    request.session['user_profile_id'] = userprofile.id
                    
                    return redirect('account:account_profile')
                
                else:
                    return render(request, 'global/account/my_login.html', {
                        'error': 'Неверный телефон или пароль!',
                        'form': form
                    })
            

            except Exception as e:

                return render(request, 'global/account/my_login.html', {
                        'error': 'Неверный телефон или пароль!',
                        'form': form
                    })
            
        else:

            return render(request, 'global/account/my_login.html', {
                        'error': 'Неверный телефон или пароль!',
                        'form': form
                    })

    

    context = {
        'form': form
    }

    return render(request, 'global/account/my_login.html', context)

from sms.views import send_sms
import random
import string

def generate_password(length):
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for i in range(length))
    return password


def my_signup(request):
    form = MySignupForm()
    if request.method == 'POST':
        


        try:

            user_profile = UserProfile.objects.get(telephone=request.POST['telephone'])
            error = 'Такой номер телефона уже зарегистрирован!'
            

            return render(request, 'global/account/my_signup.html', {
                'form': form,
                'error': error
                
                })


        except:
            form = MySignupForm(request.POST)
            

            

            if form.is_valid():
                password = [random.randint(0, 9) for i in range(4)]
                password = ''.join(map(str, password))
                user = form.save(commit=False)
                user.password = password
                user.save()

                text = f'Пароль доступа {password}'
                telephone=request.POST['telephone']

                send_sms(text, telephone)
                
                # return redirect('account:my_login')
                return redirect('account:account_profile')
            
            else:


                return render(request, 'global/account/my_signup.html', {'form': form})
            


    

    context = {
        'form': form
    }

    return render(request, 'global/account/my_signup.html', context)


from .forms import UserProfileForm
from setup.models import BaseSettings

def profile(request):

    try:
        user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])

    except:
        user_profile = None


    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            
            auto = request.POST['auto']
            vin = request.POST['vin']
            
            address = request.POST['address']
            postal_code = request.POST['postal_code']
            city = request.POST['city']
            

            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.email = email
            
            user_profile.auto = auto
            user_profile.vin = vin
            
            user_profile.address = address
            user_profile.postal_code = postal_code
            user_profile.city = city

            user_profile.save()

            return redirect('account:account_profile')
        
        else:
            print('!!!')
            return render(request, 'account/profile.html', {'profile_form': form})
                



    
        

    

    if user_profile:
        
        profile_form = UserProfileForm(instance=user_profile)

        

        context = {
            'user_profile': user_profile,
            'profile_form': profile_form
            
        }
        return render(request, 'account/profile.html', context)
    
    else:

        return redirect('account:account_signup')
    



def profile_orders(request):
    try:
        user_profile = UserProfile.objects.get(id=request.session['user_profile_id'])
    except:
        user_profile = None

    context = {
        'user_profile': user_profile
    }

    
    return render(request, 'account/profile_orders.html', context)



@login_required
def profile_wishlist(request):
    
    return render(request, 'account/profile_wishlist.html')


@login_required
def profile_history(request):
    

    context = {

    }

    return render(request, 'account/profile_history.html', context)



@login_required
def profile_update(request):
    
    context = {

    }

    return render(request, 'account/profile_update.html', context)






class LoginView(RedirectAuthenticatedUserMixin, AjaxCapableProcessFormViewMixin, FormView):
    form_class = LoginForm
    # template_name = "account/login." + app_settings.TEMPLATE_EXTENSION
    template_name = 'account/login.html'
    success_url = None
    redirect_field_name = "next"

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "login", self.form_class)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )
        return ret

    def get_context_data(self, **kwargs):
        ret = super(LoginView, self).get_context_data(**kwargs)
        signup_url = passthrough_next_redirect_url(
            self.request, reverse("account_signup"), self.redirect_field_name
        )
        redirect_field_value = get_request_param(self.request, self.redirect_field_name)
        site = get_current_site(self.request)

        ret.update(
            {
                "signup_url": signup_url,
                "site": site,
                "redirect_field_name": self.redirect_field_name,
                "redirect_field_value": redirect_field_value,
            }
        )
        return ret


login = LoginView.as_view()





class SignupView(
    RedirectAuthenticatedUserMixin,
    CloseableSignupMixin,
    AjaxCapableProcessFormViewMixin,
    FormView,
    ):
    template_name = 'account/signup.html'
    form_class = SignupForm
    redirect_field_name = "next"
    success_url = None

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "signup", self.form_class)

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )
        return ret

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        form = ret["form"]
        email = self.request.session.get("account_verified_email")
        if email:
            email_keys = ["email"]
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                email_keys.append("email2")
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(
            self.request, reverse("account_login"), self.redirect_field_name
        )
        redirect_field_name = self.redirect_field_name
        site = get_current_site(self.request)
        redirect_field_value = get_request_param(self.request, redirect_field_name)
        ret.update(
            {
                "login_url": login_url,
                "redirect_field_name": redirect_field_name,
                "redirect_field_value": redirect_field_value,
                "site": site,
            }
        )
        return ret


signup = SignupView.as_view()