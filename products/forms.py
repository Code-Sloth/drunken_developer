from django import forms
from .models import Product, Comment

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('discounted_price',)
    
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

    class Meta:
        model = Comment
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['product'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['content'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['image'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['star'].widget.attrs['class'] = 'form-control mt-1'