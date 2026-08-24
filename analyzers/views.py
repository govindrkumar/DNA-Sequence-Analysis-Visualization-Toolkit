from django.shortcuts import render
from .forms import SupportTicketForm

def index(request):
    return render(request, "analyzers/index.html")

def about_view(request):
    return render(request, "analyzers/about.html")

def analyse_view(request):
    return render(request, "analyzers/analyse.html")

def provider_view(request):
    return render(request, "analyzers/provider.html")

def issues_view(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            form.save()  # Saves My data
            form = SupportTicketForm() 
    else:
        # Jab user pehli baar page kholega (GET request), toh khali form banega
        form = SupportTicketForm()
        
    return render(request, "analyzers/issues.html", {'form': form})
