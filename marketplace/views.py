from menu.models import Category, FoodItem

from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404

from vendor.models import Vendor

def marketplace(request):
    vendors = Vendor.objects.filter(is_approval=True, user__is_active=True)
    vendors_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendors_count': vendors_count,
    }

    return render(request, 'marketplaces/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True),
        )
    )
    context = {
        'vendor': vendor,
        'categories': categories,
    }

    return render(request, 'marketplaces/vendorDetail.html', context)
