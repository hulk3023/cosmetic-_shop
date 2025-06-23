from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, CartItem




def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        if not request.session.session_key:
            request.session.create()

        cart_item, created = CartItem.objects.get_or_create(
            session_key=request.session.session_key,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

    messages.success(request, f"{product.name} savatga qo'shildi!")
    return redirect('product_list')


def cart_view(request):
    """Savatcha ko'rish"""
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)

    products = []
    subtotal = 0

    for item in cart_items:
        total_price = item.get_total_price()
        subtotal += total_price

        products.append({
            'id': item.id,
            'name': item.product.name,
            'price': item.product.price,
            'image': item.product.image,
            'quantity': item.quantity,
            'total_price': total_price,
        })

    context = {
        'title': 'Savatcha',
        'products': products,
        'subtotal': subtotal,
        'total_price': subtotal,  # Keyinchalik chegirma va yetkazib berish narxi qo'shilishi mumkin
    }

    return render(request, 'beauty/cart.html', context)


def update_cart(request):
    """Savatni yangilash (AJAX)"""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        try:
            if request.user.is_authenticated:
                cart_item = CartItem.objects.get(id=item_id, user=request.user)
            else:
                cart_item = CartItem.objects.get(id=item_id, session_key=request.session.session_key)

            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
            elif action == 'remove':
                cart_item.delete()

            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})

    return JsonResponse({'success': False})


def remove_from_cart(request, item_id):
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
        else:
            cart_item = CartItem.objects.get(id=item_id, session_key=request.session.session_key)

        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f"{product_name} savatdan o'chirildi!")
    except CartItem.DoesNotExist:
        messages.error(request, "Mahsulot topilmadi!")

    return redirect('cart_view')


def get_cart_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else:
        if request.session.session_key:
            count = CartItem.objects.filter(session_key=request.session.session_key).count()
        else:
            count = 0

    return JsonResponse({'count': count})






def checkout_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'beauty/checkout.html', context)


def confirm_order_views(request):
    if request.method == 'POST':
       name = request.POST.get('name')
       phone = request.POST.get('phone')

       return redirect('order_success')

    return redirect('checkout')



def order_success_view(request):
    return render(request, 'beauty/order_success.html')