from django import forms
from .models import Product, Comment


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