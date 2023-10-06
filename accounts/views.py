from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User
from django.contrib import messages


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # -- start create user using form
            password = form.cleaned_data['password']
            # tham so commit cho phep ban thuc hien save() va luu vao co so du lieu ngay lap tuc commit=true, hay muon thuc hien thay doi cac doi tuong roi moi luu commit=False
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            # -- end create user using form

            # -- start create data using create_user method
            user = User.objects.create_user(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            )
            user.role = User.CUSTOMER
            user.save()

            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)
