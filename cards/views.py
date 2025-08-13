from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Card Management System - Access admin panel at /admin/")
