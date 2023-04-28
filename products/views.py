from django.shortcuts import render,redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.

def index(request):
    # products = get_list_or_404(Product)
    products = Product.objects.all()
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
    return render(request, 'products/create.html', context)


# @login_required
def delete(request, product_pk):
    # product = get_object_or_404(pk=product_pk)
    product = Product.objects.get(pk=product_pk)
    if request.user == product.user:
        product.delete()
    return redirect('products:index')


# @login_required
def comment_create(request, product_pk):
    # product = get_object_or_404(pk=product_pk)
    product = Product.objects.get(pk=product_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.product = product
        comment.user = request.user
        comment.save()
        return redirect('products:detail', product_pk)
    context = {
        'product': product,
        'comment_form': comment_form,
    }
    return render(request, 'products/detail.html', context)


# @login_required
def comment_delete(request, product_pk, comment_pk):
    # comment = get_object_or_404(Comment, pk=comment_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('products:detail', product_pk)


def likes(request, product_pk):
    # product = get_object_or_404(pk=product_pk)
    product = Product.objects.get(pk=product_pk)
    if product.like_users.filter(pk=request.user.pk).exists():
        product.like_users.remove(request.user)
    else:
        product.like_users.add(request.user)
    return redirect('products:detail', product_pk)


def listing(request, category):
    # products = get_list_or_404(Product)
    products = Product.objects.all()
    if category == '전체상품':
        products = products.filter(category='전체상품')
    elif category == '전통주':
        products = products.filter(category='전통주')
    elif category == '맥주':
        products = products.filter(category='맥주')
    elif category == '위스키':
        products = products.filter(category='위스키')
    elif category == '와인':
        products = products.filter(category='와인')
    context = {
        products : 'products'
    }
    return render(request, 'products/listing.html',context)