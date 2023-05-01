from django.shortcuts import render,redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
from django.db.models import Count

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
    comments = product.comments.all().order_by('-pk')

    sort = request.GET.get('sort','')
    if sort:
        comments = comment_sort(comments, sort)

    context = {
        'product': product,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'products/detail.html', context)

def comment_sort(queryset, s):
    if s == 'recent':
        return queryset.order_by('-pk')
    elif s == 'high':
        return queryset.order_by('-star')
    else:
        return queryset.order_by('star')

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
        comment.star = int(request.POST.get('star_rating'))
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
    q = request.GET.get('q','')
    if q:
      products = Product.objects.filter(
				Q(title__icontains=q)|
				Q(content__icontains=q)|
				Q(category__icontains=q)
			)
    else: products = Product.objects.all()

    category = request.GET.get('category','')

    alcohol_percentage = request.GET.getlist('dosu','')
    a1,a2 = 100,0
    if alcohol_percentage:
        for alcohol_per in alcohol_percentage:
            a1 = min(a1,int(alcohol_per.split(',')[0]))
            a2 = max(a2,int(alcohol_per.split(',')[1]))
    else: a1,a2 = 0,100

    sweetness = request.GET.getlist('sweet',['low','middle','strong'])
    sourness = request.GET.getlist('sourness',['low','middle','strong'])
    bitterness = request.GET.getlist('bitterness',['low','middle','strong'])
    carbonated = request.GET.getlist('carbonated',['True','False'])

    price = request.GET.get('price','')
    if price: p1,p2 = price.split(',')
    else: p1,p2 = 0,1000000

    if category:
      if category == 'all':
          products = Product.objects.all()
      else:
          products = Product.objects.filter(category = category)

    products = products.filter(
        alcohol_percentage__gte=int(a1),
        alcohol_percentage__lte=int(a2),
        sweetness__in=sweetness,
        sourness__in=sourness,
        bitterness__in=bitterness,
        carbonated__in=carbonated,
        discounted_price__gte=int(p1),
        discounted_price__lte=int(p2)
    )

    sort = request.GET.get('sort','')

    products = products.annotate(num_likes=Count('like_users')).order_by('-num_likes')

    if sort:
        products = func_sort(products, sort)

    context = {
        'products': products,
        'cate': category,
    }
    return render(request, 'products/listing.html', context)

def func_sort(queryset, s):
    if s == 'recommend':
        return queryset.annotate(num_likes=Count('like_users')).order_by('-num_likes')
    elif s == 'recent':
        return queryset.order_by('-pk')
    elif s == 'rating':
        return queryset.order_by('-star')
    elif s == 'review':
        return queryset.annotate(num_comments=Count('comments')).order_by('-num_comments')
    elif s == 'high':
        return queryset.order_by('-discounted_price')
    elif s == 'low':
        return queryset.order_by('discounted_price')
