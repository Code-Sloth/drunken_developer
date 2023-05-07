from django.shortcuts import render,redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Subquery, OuterRef
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q,F
from django.db.models import Count, Avg, Max
from django.db.models import Case, When, Value, IntegerField
import requests
from django.http import JsonResponse
import openai
from dotenv import load_dotenv
import os


OPEN_API_KEY = os.getenv('OPEN_API_KEY')
KAKAO_KEY = os.getenv('KAKAO_KEY')

# Create your views here.


def index(request):
    popular_products = Product.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')
    top_latest_comments = Comment.objects.all().order_by('-star','-pk')

    top_rated_products = Product.objects.annotate(num_stars=Avg('star')).order_by('-num_stars')
    discounted_products = Product.objects.annotate(
    discount_rate_max=Max('discount_rate')
    ).annotate(
    discount_price=Case(
        When(discount_rate=F('discount_rate_max'), then=F('price') - F('price') * F('discount_rate_max') / 100),
        default=F('price'),
        output_field=IntegerField(),
    )
    ).order_by('-discount_rate_max', '-discount_price')
    context = {
        'popular_products': popular_products,
        'top_latest_comments': top_latest_comments,
        'top_rated_products': top_rated_products,
        'discounted_products': discounted_products,
    }
    return render(request, 'products/index.html', context)


def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    comments = product.comments.all().order_by('-pk')

    comment_comment_form = []
    for comment in comments:
        comment_form = CommentForm(instance=comment)
        comment_comment_form.append((comment, comment_form))

    sort = request.GET.get('sort','')
    if sort:
        comments = comment_sort(comments, sort)

        comment_comment_form = []
        for comment in comments:
            comment_form = CommentForm(instance=comment)
            comment_comment_form.append((comment, comment_form))

    context = {
        'product': product,
        'comment_comment_form': comment_comment_form,
    }
    return render(request, 'products/detail.html', context)

def comment_update(request, product_pk, comment_pk):
    product = Product.objects.get(pk=product_pk)
    comment = Comment.objects.get(pk=comment_pk)
    comment_form = CommentForm(request.POST,request.FILES, instance=comment)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.star = int(request.POST.get('star-rating'))
        comment.save()
        
        context = {
            'commentContent': comment.content,
            'commentImageUrl': comment.image.url,
            'commentStar_count': comment.star,
        }
        return JsonResponse(context)
    else:
        print(comment_form.errors)


def comment_sort(queryset, s):
    if s == 'recent':
        return queryset.order_by('-pk')
    elif s == 'high':
        return queryset.order_by('-star')
    else:
        return queryset.order_by('star')

@login_required
def kakaopay(request, product_pk):
    kakao_price = request.POST.get('kakao-price')
    kakao_count = request.POST.get('kakao-count')
    product = Product.objects.get(pk=product_pk)
    
    admin_key = KAKAO_KEY
    url = f'https://kapi.kakao.com/v1/payment/ready'
    headers = {
        'Authorization': f'KakaoAK {admin_key}',
    }
    data = {
        'cid': 'TC0ONETIME',
        'partner_order_id': product.pk, #주문 번호
        'partner_user_id': request.user.username, #유저 이름
        'item_name': product.title, #제품명
        'quantity': kakao_count, #수량
        'total_amount': kakao_price, #가격
        'tax_free_amount':'0',
 
        'approval_url':f'https://drinkit.kro.kr/products/{product.pk}/pay_success/', 
        'fail_url':'https://drinkit.kro.kr/products/pay_fail',
        'cancel_url':'https://drinkit.kro.kr/products/pay_cancel'
    }
    res = requests.post(url, data=data, headers=headers)
    result = res.json()
    request.session['tid'] = result['tid']
    return redirect(result['next_redirect_pc_url'])

@login_required
def pay_success(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    url = 'https://kapi.kakao.com/v1/payment/approve'
    admin_key = KAKAO_KEY
    
    headers = {
        'Authorization': f'KakaoAK {admin_key}'
    }
    data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'], #결제 고유 번호
        'partner_order_id': product.pk, #주문 번호
        'partner_user_id': request.user.username, #유저 아이디
        'pg_token': request.GET['pg_token'] 
    }
    res = requests.post(url, data=data, headers=headers)
    result = res.json()
    context = {
        'res':res,
        'result':result,
    }
    if result.get('msg'): #msg = 오류 코드
        return redirect('products:pay_fail')
    else:
        product.purchase_users.add(request.user, through_defaults={
            'title': product.title,
            'count': result['quantity'],
            'price': result['amount']['total']
        })
        return render(request, 'products/pay_success.html', context)

@login_required
def pay_fail(request):
    return render(request, 'products/pay_fail.html')

@login_required
def pay_cancel(request):
    return render(request, 'products/pay_cancel.html')

@user_passes_test(lambda u: u.is_superuser)
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
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('products:detail', product_pk)

@login_required
def likes(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if product.like_users.filter(pk=request.user.pk).exists():
        product.like_users.remove(request.user)
    else:
        product.like_users.add(request.user)
    return redirect('products:detail', product_pk)

def listing(request):
    q = request.GET.get('q','')
    if q:
      q = str_kr(q)
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
    elif s == 'late_low':
        return queryset.order_by('-discount_rate')

def quiz(request):
    responses = {}
    request.session['survey_data'] = {'responses': responses}

    return render(request, 'products/quiz.html', {'index': 0})

def quiz_response(request):
    survey_data = request.session.get('survey_data')
    responses = survey_data['responses']
    index = int(request.POST['index'])
    response = request.POST['response']

    responses[index] = response
    request.session['survey_data'] = survey_data

    if index < 6:
        next_index = index + 1
    else:

        if responses['1'] == 'all':
            products = Product.objects.all()
        else:
            products = Product.objects.filter(category = responses['1'])

        products = products.filter(
            alcohol_percentage__gte = int(responses['2'].split(',')[0]),
            alcohol_percentage__lte = int(responses['2'].split(',')[1]),
            sweetness__in = [responses['3'], 'middle'],
            sourness__in = [responses['4'], 'middle'],
            bitterness__in = [responses['5'], 'middle'],
            carbonated = bool(responses[6]),
        )

        if products:
            products = products.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:3]

        return render(request, 'products/quiz.html', {'products':products, 'index':7})

    return render(request, 'products/quiz.html', {'index': next_index})

def str_kr(q):
    if q == '전통주':
        return 'traditional'
    elif q == '맥주':
        return 'beer'
    elif q == '위스키':
        return 'whiskey'
    elif q == '와인':
        return 'wine'
    else:
        return q
    

openai.api_key = OPEN_API_KEY

def new_chat(request):
    messages = []

    user_content = request.POST.get('gpt-q','')

    messages.append({
        "role": "user",
        "content": f"{user_content}",
    })

    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
    )
    gptresponse = completion.choices[0].message['content'].replace('\n', '<br>')
    return JsonResponse({'gptresponse': gptresponse})
