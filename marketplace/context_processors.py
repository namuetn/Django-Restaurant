from marketplace.models import Cart

from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            carts = Cart.objects.filter(user=request.user)
            if carts:
                for cart in carts:
                    cart_count += cart.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)
