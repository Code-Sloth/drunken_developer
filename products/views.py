from django.shortcuts import render,redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
# Create your views here.

def index(request):
    # products = get_list_or_404(Product)
    products = Product.objects.all()
    context = {
        'products' : products,
    }
    return render(request, 'products/index.html',context)


def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    comment_form = CommentForm()
    comments = product.comment_set.all()
    context = {
        'product': product,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'products/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            fo = form.save(commit=False)
            fo.user = request.user
            fo.save()
            return redirect('products:index')
        else:
            print(form.errors)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'products/create.html', context)


@login_required
def delete(request, product_pk):
    # product = get_object_or_404(pk=product_pk)
    product = Product.objects.get(pk=product_pk)
    if request.user == product.user:
        product.delete()
    return redirect('products:index')


@login_required
def update(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.user == product.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('products:detail', product.pk)
        else:
            form = ProductForm(instance=product)
    else:
        return redirect('products:detail', product.pk)
    context = {
        'product' : product,
        'form' : form,
    }
    return render(request, 'products/update.html', context)


@login_required
def comment_create(request, product_pk):
    # product = get_object_or_404(pk=product_pk)
    product = Product.objects.get(pk=product_pk)
    comment_form = CommentForm(request.POST,request.FILES)
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
    return render(request, 'products/comment_create.html', context)


@login_required
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

def listing(request):
    # products = get_list_or_404(Product)
    category = request.GET.get('category','')
    alcohol_percentage = request.GET.get('dosu','')
    sweetness = request.GET.get('sweet','')
    sourness = request.GET.get('sourness','')
    bitterness = request.GET.get('bitterness','')
    carbonated = request.GET.get('carbonated','')
    price = request.GET.get('price','')
    if price: p1,p2 = price.split(',')
    else: p1,p2 = 0,1000000

    if category == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category = category)

    products = products.filter(
        alcohol_percentage__icontains=alcohol_percentage,
        sweetness__icontains=sweetness,
        sourness__icontains=sourness,
        bitterness__icontains=bitterness,
        carbonated__icontains=carbonated,
        discounted_price__gte=int(p1),
        discounted_price__lte=int(p2)
    )

    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'products/listing.html', context)

