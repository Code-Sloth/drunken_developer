from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from products.models import Purchase,Product

# Create your views here.
@login_required
def mypage(request):
    q = request.GET.get('q')
    purchases = Purchase.objects.filter(user=request.user)

    product_purchase = []
    for purchase in purchases:
        product = Product.objects.get(pk=purchase.product.pk)
        product_purchase.append((product, purchase))

    return render(request, 'accounts/mypage.html', {'q': q, 'product_purchase':product_purchase})


def login(request):
    if request.user.is_authenticated:
        return redirect('products:index')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('products:index')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form' : form,
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('products:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('products:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('products:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('products:index')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('products:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method =='POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('products:index')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context) 


def follow(request):
    User = get_user_model()
    person = User.objects.get(pk=User.pk)
    if person != request.user:
        if person.followers.fillter(pk=request.user.pk).exists():
            person.followrs.remove(request.user)
        else:
            person.followers.add(request.user)
    return redirect('accounts:mypage', person.username)
