from django.shortcuts import render,redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.

def index(request):
    products = get_list_or_404(Product)
    context = {
        'products' : products,
    }
    return render(request, 'products/index.html',context)

# @login_required
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # fo = form.save(commit=False)
            # fo.user = request.user
            form.save()
            return redirect('products:index')
        else:
            print(form.errors)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'products/create.html')
