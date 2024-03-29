from django.shortcuts import render , redirect
from django.http import HttpResponse
from . forms import userform
from . models import User , userprofile
from  django.contrib import messages , auth
from vendor.forms import vendorform
from .utils import detectuser , send_varification_email
from django.contrib.auth.decorators import login_required , user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from django.core.exceptions import PermissionDenied

# restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
# restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request , 'you are already logged in.')
        # return redirect('')
    
    elif request.method == 'POST':
        # print(request.POST)
        form = userform(request.POST)
        if form.is_valid():
            # create the user usign  the form

            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = user.CUSTOMER
            # form.save()
            # messages.success(request , 'Your account has been register sucessfully')
            # return redirect('registerUser')


            # create the user usign create_user method
        
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name , last_name=last_name , username=username , email=email , password=password)
            user.role = User.CUSTOMER
            user.save()

            # send varification email
            mail_subject = 'please activate your account'
            email_template = 'account/emails/account_varification_email.html'
            send_varification_email(request , user , mail_subject , email_template)
            
            messages.success(request , 'Your account has been register sucessfully')

            print('user is creted')
            return redirect('registerUser') 
        else:
            print('invalid form')
            print(form.errors)

    else:
        form = userform()

    context = {
        'form' : form
    }
    return render(request , 'account/registerUser.html' , context)



def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request , 'you are already logged in.')
        # return redirect('myAccount')

    elif request.method == 'POST':
        form = userform(request.POST)
        v_form = vendorform(request.POST , request.FILES)

        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name , last_name=last_name , username=username , email=email , password=password)
            user.role = User.VENDOR
            user.save()


            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = userprofile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # send varification email
            mail_subject = 'please activate your account'
            email_template = 'account/emails/account_varification_email.html'
            send_varification_email(request , user , mail_subject , email_template)

            messages.success(request , 'Your account has been register sucessfully! please wait for the approval')
            return redirect('registerVendor')


        else:
            print('invalid form')
            print(form.errors)
    else:
        form = userform()
        v_form = vendorform()

    context = {
        'form' : form,
        'v_form' : v_form
    }
    return render(request , 'account/registerVendor.html' , context)


def activate(request , uidb64 , token):
    # activate the user by setting the is_active starus is true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError , ValueError , OverflowError, User.DoesNotExist):
        user = None


    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request , 'congratulation your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request , 'invalid activation link')
        return redirect('myAccount')



def login(request):
    if request.user.is_authenticated:
        messages.warning(request , 'you are already logged in.')
        return redirect('myAccount')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email , password=password)

        if user is not None:
            auth.login(request , user)
            messages.success(request , 'you are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request , 'invalid login credentials')
            return redirect('login')
    else:
        pass
    return render(request , 'account/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request , 'you are logged out.')
    return redirect('login')

@login_required(login_url = 'login')
def myAccount(request):
    user = request.user
    redirecturl = detectuser(user)
    return redirect(redirecturl)


@login_required(login_url= 'login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request , 'account/custDashboard.html')


@login_required(login_url= 'login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request , 'account/vendorDashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            #send reset passward email
            mail_subject = 'reset your password'
            email_template = 'account/emails/reset_password_email.html'
            send_varification_email(request , user , mail_subject , email_template)

            messages.success(request , 'password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request , 'account does not exists')
            return redirect('forgot_password')

    return render(request , 'account/forgot_password.html')

def reset_password_validate(request , uidb64 , token):
    # validate the user by decoding the token and user pk  
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError , ValueError , OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request , 'please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request , 'This link has been expired!')
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['Password']
        confirm_password = request.POST['Confirm_Password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request , 'password reset sucessfully.')
            return redirect('login')
        else:
            messages.error(request , 'password do not match!')
            return redirect('reset_password')
        
    return render(request , 'account/reset_password.html')