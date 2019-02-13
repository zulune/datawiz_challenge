from django.shortcuts import render

from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    template_data = {}
    return render(request, "core/home.html", template_data)