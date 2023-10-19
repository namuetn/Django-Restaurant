from accounts.forms import UserForm
from accounts.models import User, UserProfile
from accounts.utils import detect_user, send_verification_email

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect\

from vendor.forms import VendorForm


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

@transaction.atomic
def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')

        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password'],
            )
            user.role = User.CUSTOMER
            user.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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

@transaction.atomic
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

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')

        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')

        return redirect('myAccount')

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

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            mail_subject = 'Reset your password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset link has been sent to your email address.')

            return redirect('login')
        else:
            messages.error(request, 'Account does not exist.')

            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')

        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')

        return redirect('myAccount')

@transaction.atomic
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            
            user.save()

            messages.success(request, 'Password reset successful')

            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')

            return redirect('resetPassword')
    return render(request, 'accounts/resetPassword.html')
