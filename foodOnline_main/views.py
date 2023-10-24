from django.shortcuts import render, redirect

from vendor.models import Vendor


def home(request):
    vendors = Vendor.objects.filter(is_approval=True, user__is_active=True)[:8]
    context = {
        'vendors': vendors
    }

    return render(request, 'home.html', context)
