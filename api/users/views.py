from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.

def login(request):
    return HttpResponse("hello")
