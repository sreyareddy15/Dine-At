from django.shortcuts import render
from django.http import HttpResponse
from .model import answer

def index(request):
    return HttpResponse('Hello world')

def search(request):
    location = request.POST['location']
    output = answer(location)
    return render(request,'../templates/suggestedHotel.html',{'result':output})