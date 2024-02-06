from django.shortcuts import render , redirect
from . forms import userform
from . models import user
from  django.contrib import messages

# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        # print(request.POST)
        form = userform(request.POST)
        if form.is_valid():
            # create the user usign  the form

            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = user.CUSTOMER
            form.save()
            messages.success(request , 'Your account has been register sucessfully')
            return redirect('registerUser')


            # create the user usign create_user method
        
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # user = user.objects.create_user(first_name=first_name , last_name=last_name , username=username , email=email , password=password)
            # user.role = user.CUSTOMER
            # user.save()
            # print('user is creted')
            # return redirect('registerUser') 
        else:
            print('invalid form')
            print(form.errors)

    else:
        form = userform()
    context = {
        'form' : form, 
    }
    return render(request , 'account/registerUser.html' , context)