from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from product.models import Offer, ProductImage
from .models import OrderItem, Order
from users.models import CustomUser
from product.services import get_category
from .forms import (
    OrderUserCreateForm,
    OrderPaymentCreateForm,
    OrderDeliveryCreateForm,
    OrderCardForm,
    OrderCommentForm,
)
from cart.service import Cart
from . import tasks
from django.core.cache import cache
from django.conf import settings
from random import randint

from .service import cache_data, delivery_const, delivery_total_price


class HistoryOrderView(generic.ListView):
    """
    Представление для отображения всех заказов сделанных пользователем
    """
    model = Order
    template_name = 'orders/history_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(email=self.request.user)
        context['categories'] = get_category()
        return context


class HistoryOrderDetailView(generic.DetailView):
    """
    Представление для детального отображения заказа
    """
    model = Order
    template_name = 'orders/history_order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_category()
        context['drawing'] = ProductImage.objects.all()
        context['offers'] = OrderItem.objects.filter(order=kwargs['object'])
        return context


def order_create_post(request: WSGIRequest) -> HttpResponse:
    """
    Первый этап создания заказа, информация о пользователе
    """
    if 'password' in request.POST:
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('order_create')
    form = OrderUserCreateForm(request.POST)
    if form.is_valid():
        if not request.user.is_anonymous:
            cache_data(cache, form, request)
        else:
            # Если пользователь не авторизован, но существует
            if CustomUser.objects.filter(email=form.cleaned_data['email']).exists():
                form._errors["email"] = ErrorList([_(u"Пользователь уже существует")])
                # Выводить форму входа
                return render(request, 'orders/new-order.html',
                              {'form': form, 'categories': get_category()})
            # Если пользователь не авторизован и не существует
            else:
                if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                    if form.cleaned_data.get('password1') == '':
                        form._errors["email"] = ErrorList(
                            [_(u"Данный пользователь не зарегистрирован, Введите пароль")]
                        )
                        return render(request, 'orders/new-order.html',
                                      {'form': form, 'categories': get_category()})
                    if len(form.cleaned_data.get('password1')) < 8:
                        form._errors["password1"] = ErrorList(
                            [_(u"Пароль должен быть длиннее 8 символов")]
                        )
                        return render(request, 'orders/new-order.html',
                                      {'form': form, 'categories': get_category()})
                    user = get_user_model().objects.create_user(phone=form.cleaned_data.get('number'),
                                                                email=form.cleaned_data.get('email'),
                                                                password=form.cleaned_data.get('password1'))
                    user.save()
                    user = authenticate(email=form.cleaned_data.get('email'),
                                        password=form.cleaned_data.get('password1'))
                    login(request, user)
                    cache_data(cache, form, request)
                else:
                    form._errors["password1"] = ErrorList([_(u"Пароли не совпадают")])
                    return render(request, 'orders/new-order.html',
                                  {'form': form, 'categories': get_category()})
        return redirect('order_create_delivery')
    return render(request, 'orders/new-order.html',
                  {'form': form, 'categories': get_category()})


def order_create(request: WSGIRequest) -> HttpResponse:
    """
    Первый этап создания заказа, информация о пользователе
    """
    if request.method == 'POST':
        return order_create_post(request)
    else:
        if request.user.is_authenticated:
            data = {'number': request.user.phone,
                    'email': request.user.email,
                    }
            form = OrderUserCreateForm(data)
            if request.user.phone:
                form.fields['number'].widget.attrs['readonly'] = True
            form.fields['email'].widget.attrs['readonly'] = True
            return render(request, 'orders/new-order.html',
                          {'form': form, 'categories': get_category()})
        else:
            form = OrderUserCreateForm
            return render(request, 'orders/new-order.html',
                          {'form': form, 'categories': get_category()})


def order_create_delivery(request: WSGIRequest) -> HttpResponse:
    """
    Второй этап создания заказа, информация о доставке
    """
    if request.method == 'POST':
        form = OrderDeliveryCreateForm(request.POST)
        if form.is_valid():
            cache.set('delivery', form.cleaned_data.get('delivery'))
            cache.set('city', form.cleaned_data.get('city'))
            cache.set('address', form.cleaned_data.get('address'))
            return redirect('order_type_payment')
    else:
        form = OrderDeliveryCreateForm
    return render(request, 'orders/order-delivery.html',
                  {'form': form, 'categories': get_category()})


def order_type_payment(request: WSGIRequest) -> HttpResponse:
    """
    Третий этап создания заказа, информация о типе оплаты
    """
    if request.method == 'POST':
        form = OrderPaymentCreateForm(request.POST)
        if form.is_valid():
            cache.set('payment', form.cleaned_data.get('payment'))
            return redirect('order_create_comment')
    else:
        form = OrderPaymentCreateForm
    return render(request, 'orders/order-payment.html',
                  {'form': form, 'categories': get_category()})


def order_create_comment(request: WSGIRequest) -> HttpResponse:
    """
    Четвертый  этап создания заказа, вывод основной информации
    """
    cart = Cart(request)
    elem = request.session.get(settings.ADMIN_SETTINGS_ID)
    delivery_price = delivery_const(elem, 'DELIVERY_PRICE', settings.DELIVERY_PRICE)
    delivery_stock = delivery_const(elem, 'DELIVERY_STOCK', settings.DELIVERY_STOCK)
    delivery_express = delivery_const(elem, 'DELIVERY_EXPRESS', settings.DELIVERY_EXPRESS)
    total = delivery_total_price(cache, cart, delivery_express, delivery_price, delivery_stock)
    status = 'Ожидание ответа от продавца'
    cache.set('total', total)
    cache.set('status', status)
    data = {'first_name': cache.get('first_name'), 'last_name': cache.get('last_name'), 'email': cache.get('email'),
            'number': cache.get('number'), 'delivery': cache.get('delivery'), 'city': cache.get('city'),
            'address': cache.get('address'), 'payment': cache.get('payment'), 'total': total, 'status': status
            }
    if request.method == 'POST':
        form = OrderCommentForm(request.POST)
        if form.is_valid():
            cache.set('comment', form.cleaned_data.get('comment'))
            return redirect('order_create_payment')
    else:
        form = OrderCommentForm
    return render(request, 'orders/order-comment.html',
                  {'form': form, 'categories': get_category(), 'data': data})


def order_create_payment(request: WSGIRequest) -> HttpResponse:
    """
    Четвертый этап создания заказа, и процесс оплаты
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCardForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(first_name=cache.get('first_name'),
                                         last_name=cache.get('last_name'),
                                         email=cache.get('email'),
                                         number=cache.get('number'),
                                         delivery=cache.get('delivery'),
                                         status=cache.get('status'),
                                         city=cache.get('city'),
                                         address=cache.get('address'),
                                         payment=cache.get('payment'),
                                         card_number=form.cleaned_data.get('card_number'),
                                         total=cache.get('total'),
                                         comment=cache.get('comment'))
            for item in cart.cart:
                OrderItem.objects.create(order=order,
                                         offer=Offer.objects.get(id=int(item)),
                                         price=float(cart.cart[item]['price']),
                                         quantity=cart.cart[item]['quantity'],
                                         )
            cart.clear()
            cache.close()
            tasks.payment.delay(order.pk)
            return redirect('wait-payment', pk=order.pk)
    else:
        if cache.get('payment') == 'F':
            form = OrderCardForm({'card_number': randint(10000000, 99999999)})
            return render(request, 'orders/order.html',
                          {'form': form, 'categories': get_category(), 'rand': True})
        else:
            form = OrderCardForm()

    return render(request, 'orders/order.html',
                  {'form': form, 'categories': get_category()})


def wait_payment(request: WSGIRequest, pk) -> HttpResponse:
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/created.html', {'order': order})
