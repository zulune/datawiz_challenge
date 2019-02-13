from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.views.generic import View, FormView

from .forms import SignUpForm, SignInForm
# Create your views here.


@login_required(login_url="/login/")
def home(request):
    template_data = {}
    return render(request, "core/home.html", template_data)


class GuestOnly(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')

        return super().dispatch(request, *args, **kwargs)


class SignUpFormView(GuestOnly, FormView):
    template_name = 'registration/register.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']
        user = get_user_model().objects.create_user(
            username=email.split('@', )[0],
            email=email)
        user.username = f'user_{user.id}'
        user.set_password(password)
        user.save()
        return redirect('code:login')


class SignInFormView(GuestOnly, FormView):
    template_name = 'registration/login.html'
    form_class = SignInForm

    def form_valid(self, form):
        request = self.request

        login(request, form.user_cache, 
            backend='core.backends.UserModelEmailBackend'
        )
        return redirect('/')