from django.shortcuts import render, redirect
from .forms import SupportTicketForm, SequenceUploadForm
from .models import UploadedSequence

from Bio import SeqIO as bq
from Bio.SeqUtils import gc_fraction

import io


def index(request):
    return render(request, "analyzers/index.html")


def about_view(request):
    return render(request, "analyzers/about.html")


def analyse_view(request):

    if request.method == 'POST':
        form = SequenceUploadForm(request.POST, request.FILES)

        if form.is_valid():

            uploaded_file = form.cleaned_data['file']

            if uploaded_file.name.lower().endswith(('.gb', '.fasta')):
                sequence = UploadedSequence.objects.create(
                    file=uploaded_file
                )

                return redirect(
                    'run_analysis',
                    sequence_id=sequence.id
                )

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

    # Move to beginning of file
    uploaded_file.seek(0)

    # Convert Django's binary uploaded file into text
    text_file = io.TextIOWrapper(
        uploaded_file,
        encoding='utf-8'
    )

    # Decide format from file extension
    if uploaded_file.name.lower().endswith('.fasta'):

        record = next(
            bq.parse(text_file, 'fasta')
        )

    elif uploaded_file.name.lower().endswith(('.gb', '.genbank')):

        record = next(
            bq.parse(text_file, 'genbank')
        )

    else:
        return render(
            request,
            "analyzers/result.html",
            {
                'error': 'Unsupported file format.'
            }
        )

    # Basic sequence information
    a = record.id
    b = record.description
    c = record.seq
    d = record.annotations
    e = record.features

    # Feature information
    feature_types = []
    feature_locations = []
    feature_qualifiers = []

    for feature in record.features:

        feature_types.append(feature.type)
        feature_locations.append(feature.location)
        feature_qualifiers.append(feature.qualifiers)

    # Sequence statistics
    gc = gc_fraction(record.seq) * 100
    length = len(record.seq)

    return render(
        request,
        "analyzers/result.html",
        {
            'record_id': a,
            'record_description': b,
            'record_seq': c,
            'record_annotations': d,
            'record_features': e,
            'record_types': feature_types,
            'record_locations': feature_locations,
            'record_qualifiers': feature_qualifiers,
            'gc_fraction': gc,
            'gene_length': length,
        }
    )


def provider_view(request):
    return render(
        request,
        "analyzers/provider.html"
    )


def issues_view(request):

    if request.method == 'POST':

        form = SupportTicketForm(request.POST)

        if form.is_valid():
            form.save()
            form = SupportTicketForm()

    else:
        form = SupportTicketForm()

    return render(
        request,
        "analyzers/issues.html",
        {'form': form}
    )