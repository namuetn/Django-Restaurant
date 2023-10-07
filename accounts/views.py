from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import detect_user
from vendor.forms import VendorForm
from django.core.exceptions import PermissionDenied

# Retrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    raise PermissionDenied
    
# Retrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    raise PermissionDenied

def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')

        return redirect('dashboard')
    elif request.method == 'POST':
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

            messages.success(request, 'Your account has been registered successfully!')

            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }

    return render(request, 'accounts/registerUser.html', context)

def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')

        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            user = User.objects.create_user(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            )
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            messages.success(request, 'Your account has been registered successfully! Please wait for the approval')

            return redirect('registerVendor')
        else:
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')

        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')

            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid logged credentials.')

            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')

    return redirect('login')

@login_required(login_url='login')
def my_account(request):
    user = request.user
    redirectUrl = detect_user(user)

    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor) # Mục tiêu của decorator này là đảm bảo rằng chỉ có các nhà cung cấp (vendors) mới được phép truy cập vào trang vendor_dashboard.
def vendor_dashboard(request):
    return render(request, 'accounts/vendorDashboard.html')
