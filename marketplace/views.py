from menu.models import Category, FoodItem

from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from marketplace.context_processors import get_cart_counter
from marketplace.models import Cart

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

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    else:
        carts = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'carts': carts
    }

    return render(request, 'marketplaces/vendorDetail.html', context)

def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)

                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    checkCart.quantity += 1
                    checkCart.save()

                    return JsonResponse({'status': 'Success', 'message': 'Increase the cart quantity', 'cart_counter': get_cart_counter(request), 'quantity': checkCart.quantity})
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)

                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'quantity': checkCart.quantity})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)

                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)

                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0

                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'quantity': checkCart.quantity})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not this item in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

