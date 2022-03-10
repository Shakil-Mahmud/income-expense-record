import email
import imp
from lib2to3.pgen2 import token
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_activation_token
# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({"email_error": "Email is invalid"})
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Email already exist"})
        return JsonResponse({"email_valid": True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error": "User should contain only number and alphabet"})
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "This user name already exist"})
        return JsonResponse({"username_valid": True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                link= reverse('activate', kwargs=
                            {'uidb64':uidb64, 'token':token})
                activate_url = 'http://'+domain+link

                email_subject = 'test mail'
                email_body = 'Clicked the link below to activate you account.\n'+activate_url
                the_email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@gmail.com',
                    [email],
                )
                the_email.send(fail_silently=False)

                messages.success(request, 'Account successfully created')
                return redirect('login')

        return render(request, 'authentication/register.html')    



class VerificationView(View):
    def get(self, request, uidb64, token):
        print('here ')
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)
        print('here 1')

        if not account_activation_token.check_token(user, token):
            return redirect('login'+'?message='+'User is already activated.')
        print('here 2')
        if user.is_active:
            return redirect('login')
        print('here 3')
        user.is_active = True
        user.save()

        print('here 4')
        messages.success(request, "The account is activated successfully ")
#        return redirect('login')
            
        return redirect('login' )


###############################################
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
