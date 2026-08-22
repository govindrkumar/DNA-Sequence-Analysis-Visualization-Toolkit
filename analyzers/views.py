from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'analyzers/index.html')

#adding about page
def about(request):
    return render(request, 'analyzers/about.html')