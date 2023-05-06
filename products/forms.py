from django import forms
from .models import Product, Comment

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title','content','price','discount_rate','category','alcohol_percentage','sweetness','sourness','bitterness','carbonated','volume','delivery_date','image')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['content'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['price'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['discount_rate'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['category'].widget.attrs['class'] = 'form-select mt-1'
        self.fields['alcohol_percentage'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['sweetness'].widget.attrs['class'] = 'form-select mt-1'
        self.fields['sourness'].widget.attrs['class'] = 'form-select mt-1'
        self.fields['bitterness'].widget.attrs['class'] = 'form-select mt-1'
        self.fields['carbonated'].widget.attrs['class'] = 'form-check mt-1'
        self.fields['volume'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['delivery_date'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['image'].widget.attrs['class'] = 'form-control mt-1'

class CommentForm(forms.ModelForm):
    image = forms.ImageField(
        label = False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

    class Meta:
        model = Comment
        fields = ('content','image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['content'].widget.attrs['placeholder'] = '다른 고객님에게 도움이 되도록 상품에 대한 솔직한 평가를 남겨주세요.'
        self.fields['image'].widget.attrs['class'] = 'form-control mt-1'
