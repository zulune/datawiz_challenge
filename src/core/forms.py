from django import forms
from django.forms import ValidationError

from django.contrib.auth import get_user_model

User = get_user_model()


class UserCacheMixin:
    user_cache = None


class SignUpForm(forms.ModelForm):
    """
        Кастомна форма реєстрації на сайті
        з використанням обов'язкового введення
        електроної пошти
    """
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'palceholder': 'Password'}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'palceholder': 'Confirm Password'}
    ))

    # Модифікацію поля псевдоніма користувача
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email'}
        )

    class Meta:
        model = User
        fields = ('email', )

    # Валідація унікальної електроної почти
    def clean_email(self):
        email = super().clean()
        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError('You can not use this email address')
        return email

    # Перевірка на правильність введення паролю
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if (password1 != password2):
            raise ValidationError('Password1 and Password2 must mutch!')


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(
        label=('Password'),
        strip=False,
        widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.__dict__.get('user_cache'):
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError("You enter invalid password!")
        return password


class SignInForm(SignIn):
    email = forms.EmailField(label=('Email'))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError('You entered invalid password')

        user.user_cache = user
        return email