# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    Link budget input page
    """
    return render(request, "linkbudget/index.html")


