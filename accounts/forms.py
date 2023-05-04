from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username',
            'email',
            'last_name',
            'password1',
            'password2',
            'gender',
            'birthday',
            'image',
        )
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control mt-1',
                'type': 'date',
            }
        ),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['username'].widget.attrs['placeholder'] = '아이디'
        self.fields['email'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['email'].widget.attrs['placeholder'] = '이메일'
        self.fields['last_name'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['last_name'].widget.attrs['placeholder'] = '이름'
        self.fields['password1'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['password1'].widget.attrs['placeholder'] = '비밀번호'
        self.fields['password2'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['password2'].widget.attrs['placeholder'] = '비밀번호 확인'
        self.fields['gender'].widget.attrs['class'] = 'form-select mt-1'
    

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'last_name', 'image',)

    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control mt-1',
            }
        ),
        required=False
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['email'].widget.attrs['placeholder'] = '이메일'
        self.fields['last_name'].widget.attrs['class'] = 'form-control mt-1'
        self.fields['last_name'].widget.attrs['placeholder'] = '이름'


class CustomAuthenticationForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        model = get_user_model()
        fields = ('username','password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = '아이디를 입력해 주세요'

        self.fields['password'].widget.attrs['placeholder'] = '비밀번호를 입력해 주세요'

