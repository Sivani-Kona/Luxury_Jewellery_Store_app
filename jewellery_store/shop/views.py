from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total
    })


@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)

    total = 0

    for item in items:
        item_total = item.product.price * item.quantity

        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=item_total
        )

        total += item_total

    items.delete()

    return render(request, 'shop/checkout.html', {
        'total': total
    })

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'shop/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'shop/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'shop/orders.html', {
        'orders': orders
    })
