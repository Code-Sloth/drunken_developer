# Generated by Django 3.2.18 on 2023-04-27 08:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('content', models.TextField()),
                ('price', models.IntegerField()),
                ('discount_rate', models.IntegerField(default=0)),
                ('discounted_price', models.IntegerField()),
                ('category', models.CharField(choices=[('전체상품', '전체상품'), ('전통주', '전통주'), ('맥주', '맥주'), ('위스키', '위스키'), ('와인', '와인')], max_length=20)),
                ('alcohol_percentage', models.IntegerField()),
                ('sweetness', models.CharField(choices=[('약한', '약한'), ('중간', '중간'), ('강한', '강한')], max_length=20)),
                ('sourness', models.CharField(choices=[('약한', '약한'), ('중간', '중간'), ('강한', '강한')], max_length=20)),
                ('bitterness', models.CharField(choices=[('약한', '약한'), ('중간', '중간'), ('강한', '강한')], max_length=20)),
                ('carbonated', models.BooleanField()),
                ('volume', models.IntegerField()),
                ('delivery_date', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=products.models.Product.product_image_path)),
                ('like_users', models.ManyToManyField(related_name='like_products', to='accounts.User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=products.models.Comment.comment_image_path)),
                ('star', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
