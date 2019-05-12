from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    response = redirect('/bookDetails/')
    return response

def login(request):
    return HttpResponse("This is the login page")

def signup(request):
    return HttpResponse("This is the signup page")

