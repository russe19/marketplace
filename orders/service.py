from product.models import Offer


def cache_data(cache, form, request):
    cache.set('first_name', form.cleaned_data.get('first_name'))
    cache.set('last_name', form.cleaned_data.get('last_name'))
    cache.set('email', request.user.email)
    cache.set('number', form.cleaned_data.get('number'))


def delivery_const(elem, elem_value, setting_value):
    if elem is None or elem[elem_value] is None:
        return setting_value
    return elem[elem_value]


def delivery_total_price(cache, cart, delivery_express, delivery_price, delivery_stock):
    seller_list = []
    total = cart.get_total_price()
    if cache.get('delivery') == 'A':
        total += delivery_express
    else:
        for item in cart:
            seller_list.append(Offer.objects.get(id=item['product'].id).seller)
            seller_list = set(seller_list)
        if total < delivery_price or len(seller_list) > 1:
            total += delivery_stock
    return total
