from django.shortcuts import render


def vendor_profile(request):
    return render(request, 'vendors/profile.html')
