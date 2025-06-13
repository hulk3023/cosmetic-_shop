from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout



class ProductList(ListView):
    model = Product
    extra_context = {
        'title': 'Beauty Store',
    }
    template_name = 'beauty/product_list.html'


def home(request):
    featured_products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    new_arrivals = Product.objects.filter(is_available=True).order_by('-created_at')[:4]
    sale_products = Product.objects.filter(is_available=True, sale_price__isnull=False).order_by('?')[:4]
    popular_categories = Category.objects.all()[:6]

    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'sale_products': sale_products,
        'popular_categories': popular_categories,
    }
    return render(request, 'home.html', context)


def product_list(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'beauty/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form
    }

    return render(request, 'beauty/product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product = get_object_or_404(Product, slug=slug)

    # O'rtacha reytingni hisoblash
    avg_rating = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    return render(request, 'beauty/product_detail.html', {
        'product': product,
        'avg_rating': avg_rating,
    })


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = Product.objects.filter(brand=brand, is_available=True)

    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'brand': brand,
        'page_obj': page_obj,
    }
    return render(request, 'beauty/brand_detail.html', context)


def search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        ).filter(is_available=True)
    else:
        products = Product.objects.none()

    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'beauty/search_results.html', context)


def login_registration(request):
    context = {
        'title': 'Login and Registration',
        'login_form': LoginForm(),
        'register_form': RegisterForm(),
    }
    return render(request, 'beauty/login_registration.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli kirildi!')
            return redirect('product_list')
        else:
            messages.error(request, 'Username yoki parol noto\'g\'ri!')
            context = {
                'title': 'Login and Registration',
                'login_form': form,
                'register_form': RegisterForm(),
            }
            return render(request, 'beauty/login_registration.html', context)
    else:
        return redirect('login_registration')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Hisob yaratildi! {user.username}')

            # Avtomatik login qilish
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Formada xatoliklar mavjud!')
            context = {
                'title': 'Login and Registration',
                'login_form': LoginForm(),
                'register_form': form,
            }
            return render(request, 'beauty/login_registration.html', context)
    else:
        return redirect('login_registration')


def user_logout(request):
    logout(request)
    return redirect('user_login')


def cart_detail(request):

    return render(request, 'beauty/cart_detail.html')



def sovunlar_product_list(request):
	products = Product.objects.filter(category='sovunlar')
	return render(request, 'sovunlar.html', {'products': products})

