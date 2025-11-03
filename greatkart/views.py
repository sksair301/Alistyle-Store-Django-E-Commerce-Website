from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from stores.models import Products
from category.models import Category

def home(request):
    products = Products.objects.all().filter(is_available = True)
    category = Category.objects.all()
    
    context={
        'products' : products,
        'category' : category,
    }
    return render(request,'home.html',context,)


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # ✅ Basic validations
        if password1 != password2:
            messages.error(request, "Passwords do not match ❌")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists ⚠️")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already registered ⚠️")
            return redirect("signup")

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()

        messages.success(request, "Account created successfully 🎉 Please log in!")
        return redirect("login_view")

    return render(request,'signup.html')


def login_view(request):
    # If user already logged in
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')  # message will show on home

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # ⚠️ Handle empty fields → message shown on login page
        if not username or not password:
            messages.warning(request, "⚠️ Please fill in both username and password.")
            return render(request, 'login.html')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ✅ Successful login → redirect to home with success message
            auth_login(request, user)
            messages.success(request, f"✅ Welcome back, {user.username}!")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'home')

        else:
            # ❌ Invalid credentials → message shown on login page
            messages.error(request, "❌ Invalid username or password.")
            return render(request, 'login.html')

    # GET → just render the login form
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You’ve been logged out successfully 👋")
    return redirect('login_view')
