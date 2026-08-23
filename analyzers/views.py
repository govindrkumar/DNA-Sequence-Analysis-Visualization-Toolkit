from django.shortcuts import render
from .forms import paste_data

def index(request):
    form = paste_data()
    return render(request, "analyzers/index.html", {"form": form})

def about_view(request):
    return render(request, "analyzers/about.html")

def analyse_view(request):
    return render(request, "analyzers/analyse.html")

def provider_view(request):
    return render(request, "analyzers/provider.html")

def issues_view(request):
    return render(request, "analyzers/issues.html")

