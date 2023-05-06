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
                'type': 'date',
            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = '아이디를 입력해 주세요'
        self.fields['email'].widget.attrs['placeholder'] = '이메일을 입력해 주세요'
        self.fields['last_name'].widget.attrs['placeholder'] = '이름을 입력해 주세요'
        self.fields['password1'].widget.attrs['placeholder'] = '비밀번호를 입력해주세요'
        self.fields['password2'].widget.attrs['placeholder'] = '비밀번호 다시 입력해주세요'
        self.fields['image'].widget.attrs['class'] = 'form-control'
    

class CustomUserChangeForm(UserChangeForm):
    image = forms.ImageField(
        label = False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'last_name', 'image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = '이메일을 입력해 주세요'
        self.fields['last_name'].widget.attrs['placeholder'] = '이름을 입력해 주세요'


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = '아이디를 입력해 주세요'
        self.fields['password'].widget.attrs['placeholder'] = '비밀번호를 입력해 주세요'

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['placeholder'] = '현재 비밀번호를 입력해 주세요'
        self.fields['new_password1'].widget.attrs['placeholder'] = '새 비밀번호를 입력해 주세요'
        self.fields['new_password2'].widget.attrs['placeholder'] = '새 비밀번호를 다시 입력해 주세요'