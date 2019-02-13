from django.shortcuts import render

# Create your views here.


def home(request):
    template_data = {}
    return render(request, "core/home.html", template_data)