from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta,datetime

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_products')
    purchase_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='purchase_products', through='Purchase')

    star = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    price = models.IntegerField()
    discount_rate = models.IntegerField(default=0)
    discounted_price = models.IntegerField()

    category_Choices = (('all','전체상품') ,('traditional','전통주'), ('beer','맥주'), ('whiskey','위스키'), ('wine','와인'))
    category = models.CharField(max_length=20, choices=category_Choices)

    alcohol_percentage = models.DecimalField(max_digits=100,decimal_places=1)

    sweetness_Choices = (('low','약한') ,('middle','중간'), ('strong','강한'))
    sweetness = models.CharField(max_length=20, choices=sweetness_Choices)

    sourness_Choices = (('low','약한') ,('middle','중간'), ('strong','강한'))
    sourness = models.CharField(max_length=20, choices=sourness_Choices)

    bitterness_Choices = (('low','약한') ,('middle','중간'), ('strong','강한'))
    bitterness = models.CharField(max_length=20, choices=bitterness_Choices)

    carbonated = models.BooleanField()

    volume = models.IntegerField()

    delivery_date = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def product_image_path(instance, filename):
        return f'products/{instance.title}/{filename}'
    
    image = ProcessedImageField(
        upload_to=product_image_path,
        processors=[ResizeToFill(320,426)],
        format='JPEG',
        options={'quality' : 100},
        blank=True,
        null=True,
    )

    def calculate_discount_price(self):
        return round((self.price * (1 -self.discount_rate / 100)) / 10) * 10
    
    def save(self,*args, **kargs):
        self.discounted_price = self.calculate_discount_price()
        super().save(*args, **kargs)
    
    @property
    def star_multiple(self):
        return self.star*20

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    count = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def created_string_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_time

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_time.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def comment_image_path(instance, filename):
        return f'comments/{instance.user.username}/{filename}'

    image = ProcessedImageField(
        upload_to=comment_image_path,
        processors=[ResizeToFill(270,270)],
        format='JPEG',
        options={'quality' : 100},
        blank=True,
        null=True,
    )

    star = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])

    @property
    def created_time(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')

    @property
    def star_multiple(self):
        return self.star*20
    
    def save(self, *args, **kwargs):
        self.product.star = (self.product.star * self.product.comments.count() + self.star) / (self.product.comments.count() + 1)
        self.product.save()
        super(Comment, self).save(*args, **kwargs)
