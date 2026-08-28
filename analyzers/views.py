from django.shortcuts import render, redirect
from .forms import SupportTicketForm, SequenceUploadForm
from .models import UploadedSequence

def index(request):
    return render(request, "analyzers/index.html")

def about_view(request):
    return render(request, "analyzers/about.html")

def analyse_view(request):

    if request.method == 'POST':
        form = SequenceUploadForm(request.POST, request.FILES)

        if form.is_valid():

            uploaded_file = form.cleaned_data['file']

            sequence = UploadedSequence.objects.create(
                file=uploaded_file
            )

            return redirect('run_analysis', sequence_id=sequence.id)

    else:
        form = SequenceUploadForm()

    return render(
        request,
        "analyzers/analyse.html",
        {'form': form}
    )


def run_analysis(request, sequence_id):

    sequence = UploadedSequence.objects.get(id=sequence_id)

    uploaded_file = sequence.file

    print(uploaded_file.name)

    # Ab yahan:
    # Biopython
    # Pandas
    # sequence analysis
    # etc.

    return render(
        request,
        "analyzers/result.html"
    )


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
