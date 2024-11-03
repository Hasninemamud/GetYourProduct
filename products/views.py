from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Product, Cart, CartItem, Order, Profile
from .forms import UserProfileForm, RegistrationForm

# Product Views

from django.shortcuts import render
from django.db.models import Q
from .models import Product

def product_list(request):
    query = request.GET.get('query', '')  # Get the search query, defaulting to an empty string
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query,
    })





def product_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else []
    
    return render(request, 'product_search.html', {
        'products': products,
        'query': query,
    })

# Cart and Order Views

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Cart  # Ensure you have a Cart model to manage the cart

from django.shortcuts import redirect
from django.contrib import messages
from .models import Cart, Product  # Import your models
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, Product  # Adjust the import based on your models
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, Product  # Adjust the import based on your models

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        # Retrieve the product_id from POST data
        product_id = request.POST.get('product_id')

        # Use get_object_or_404 to fetch the product or return a 404 error if not found
        product = get_object_or_404(Product, id=product_id)

        # Logic to add the product to the cart
        # Assuming you have a Cart model and a ManyToMany relationship with Product
        cart, created = Cart.objects.get_or_create(user=request.user)  # Modify as per your cart logic
        cart.products.add(product)  # Add the product to the cart

        # Success message
        messages.success(request, f'{product.name} has been added to your cart!')

        # Redirect back to the product list or any other page
        return redirect('product_list')

    # Redirect if the request method is not POST
    return redirect('product_list')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Review
from .forms import ReviewForm

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been added.")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'product': product})

# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     reviews = product.reviews.all()  # Fetch all reviews for this product
#     return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

from .models import Product, Review

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)  # Fetch reviews for this product
    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews
    })

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'products/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_item_count': cart_items.count(),
    })

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem, Order

@login_required

def place_order(request):
    # Retrieve the cart and its items for the current user
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Redirect to cart if no items are found
    if not cart_items.exists():
        return redirect('cart_detail')

    # Calculate the total order amount
    order_total = sum(item.product.price * item.quantity for item in cart_items)

    # Place an order for each cart item
    for item in cart_items:
        # Create an Order object with "Pending" status by default
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            # status="Confirmed" if item.product.stock >= item.quantity else "Pending"  # Example condition
        )

    # Clear the cart after placing the order
    cart_items.delete()

    # Render the order confirmation page with the total amount
    return render(request, 'products/order_confirmation.html', {'order_total': order_total})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'products/order_history.html', {'orders': orders})

# Profile View

from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to a success page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def profile_view(request):
    profile_instance = request.user.profile  # Assuming you have a OneToOne relationship
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user, profile_instance=profile_instance)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to a success page
    else:
        form = UserProfileForm(instance=request.user, profile_instance=profile_instance)
    return render(request, 'profile.html', {'form': form})

# Authentication Views

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



def about(request):
    return render(request, 'about.html')


from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category__id=category_id)
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()  # To display category options

    context = {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'products/product_list.html', context)
