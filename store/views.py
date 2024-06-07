from django.shortcuts import render

# Create your views here.

from .models import Product

# 產品首頁
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# 關於我們
def about(request):
    return render(request, 'store/about.html')

# 在 store/views.py 文件中追加
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem

@login_required(login_url='/admin/') # 檢測使用者是否登入，若登入才會執行
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('product_list')

@login_required(login_url='/admin/')
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    return render(request, 'store/view_cart.html', {'cart':cart, 'total_price':total_price})

# @login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
    if request.method == 'POST':
        # 模擬付款成功的情況
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart.cartitem_set.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart.cartitem_set.all().delete()
        return redirect('order_success') # 將用戶導向成功的頁面
    return render(request, 'store/checkout.html', {'cart':cart, 'total_price':total_price})

def order_success(request):
    return render(request, 'store/order_success.html')
