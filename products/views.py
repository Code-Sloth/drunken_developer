from django.shortcuts import render,redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.

