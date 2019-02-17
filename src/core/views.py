import json
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.views.generic import View, FormView

from .forms import SignUpForm, SignIn

from .analitycs.data_api import DatawizInfo
# Create your views here.


@login_required(login_url="/login/")
def home(request):
    di = DatawizInfo('test1@mail.com', '1gaz')
    shops = di.get_shops()
    product_sale_data = dict()
    now = date.today()
    from_date = now - timedelta(days=10)
    for shop in shops:
        product_sale_data['shops'] = shop
    product_sale_data['products'] = list()
    product_sale_data['date_to'] = now
    product_sale_data['date_from'] = from_date
    products_sale = di.get_products_sale(**product_sale_data)
    client_info = di.get_client_info()
    template_data = {'shops': shops, 'client_info': client_info}
    return render(request, "core/home.html", template_data)


def get_shop_info(request):
    if request.POST is ajax:
        print('AJAX')
        return JsonResponse({'data': 'ajax'})


class SignUpFormView(FormView):
    template_name = 'registration/register.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = get_user_model().objects.create_user(
            username=username,
            email=email)
        user.set_password(password)
        user.save()
        return redirect('code:login')


class SignInFormView(FormView):
    template_name = 'registration/login.html'
    form_class = SignIn
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return super().form_valid(form)