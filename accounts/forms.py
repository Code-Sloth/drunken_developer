from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'image',
        )
    
    username = forms.CharField(
        label='아이디',
        required=True,
    )
    email = forms.CharField(
        label='이메일',
        required=True,
    )

    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'image',)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'first_name', 'last_name', 'image',]:
            self.fields[fieldname].help_text = None