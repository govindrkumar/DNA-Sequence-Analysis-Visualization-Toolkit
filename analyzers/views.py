from django.shortcuts import render, redirect
from .forms import SupportTicketForm, SequenceUploadForm
from .models import UploadedSequence

from Bio import SeqIO as bq
from Bio.SeqUtils import gc_fraction, molecular_weight
from Bio.SeqUtils.MeltingTemp import Tm_Wallace
from Bio.Blast import NCBIWWW
from datetime import date

import matplotlib
matplotlib.use('Agg')  # GUI nahi chahiye, sirf image banana hai
import matplotlib.pyplot as plt
import base64
from io import BytesIO, TextIOWrapper


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


def make_chart(xt, yt, xlabel, ylabel, title, color='teal'):
    """Helper function — chart banao aur base64 return karo"""
    plt.figure(figsize=(6, 3))
    plt.barh(xt, yt, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return chart


def run_analysis(request, sequence_id):

    sequence = UploadedSequence.objects.get(id=sequence_id)
    uploaded_file = sequence.file

    print(uploaded_file.name)

    uploaded_file.seek(0)
    text_file = TextIOWrapper(uploaded_file, encoding='utf-8')

    # Format detect karo
    if uploaded_file.name.lower().endswith('.fasta'):
        record = next(bq.parse(text_file, 'fasta'))
        seq = str(record.seq).upper()

        if set(seq) <= set("ACGTN"):
            sequence_type = "DNA"
        elif set(seq) <= set("ACGUN"):
            sequence_type = "RNA"
        else:
            sequence_type = "Protein"

    elif uploaded_file.name.lower().endswith(('.gb', '.genbank')):
        record = next(bq.parse(text_file, 'genbank'))
        sequence_type = record.annotations.get('molecule_type')

    else:
        return render(
            request,
            "analyzers/result.html",
            {'error': 'Unsupported file format.'}
        )

    # Basic info
    analysis_date = date.today()
    protein_seq = str(record.seq.translate())

    # Feature info
    feature_types = []
    feature_locations = []
    feature_qualifiers = []

    for feature in record.features:
        feature_types.append(feature.type)
        feature_locations.append(feature.location)
        feature_qualifiers.append(feature.qualifiers)

    # Sequence statistics
    length = len(record.seq)
    gc = gc_fraction(record.seq) * 100
    mol_weight = molecular_weight(record.seq)
    tm = Tm_Wallace(record.seq)

    # Base counts
    a_count = record.seq.count('A')
    t_count = record.seq.count('T')
    g_count = record.seq.count('G')
    c_count = record.seq.count('C')

    # Percentages
    a_perc = round((a_count / length) * 100, 2)
    t_perc = round((t_count / length) * 100, 2)
    g_perc = round((g_count / length) * 100, 2)
    c_perc = round((c_count / length) * 100, 2)

    # GC vs AT chart
    gc_count = g_count + c_count
    at_count = a_count + t_count
    at_gc_chart = make_chart(
        xt=['GC', 'AT'],
        yt=[gc_count, at_count],
        xlabel='Count',
        ylabel='Type',
        title='AT vs GC Content'
    )

    # A T G C chart
    base_chart = make_chart(
        xt=['A', 'T', 'G', 'C'],
        yt=[a_count, t_count, g_count, c_count],
        xlabel='Count',
        ylabel='Base',
        title='Nucleotide Distribution',
        color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    )

    return render(
        request,
        "analyzers/result.html",
        {
            'record_id': record.id,
            'record_description': record.description,
            'record_seq': record.seq,
            'record_annotations': record.annotations,
            'record_features': record.features,
            'record_types': feature_types,
            'record_locations': feature_locations,
            'record_qualifiers': feature_qualifiers,
            'gc_fraction': round(gc, 2),
            'gene_length': length,
            'protein_seq': protein_seq,
            'sequence_type': sequence_type,
            'analysis_date': analysis_date,
            'a_count': a_count,
            't_count': t_count,
            'g_count': g_count,
            'c_count': c_count,
            'mol_weight': round(mol_weight, 2),
            'tm': round(tm, 2),
            'a_perc': a_perc,
            't_perc': t_perc,
            'g_perc': g_perc,
            'c_perc': c_perc,
            'at_gc_chart': at_gc_chart,
            'base_chart': base_chart,
        }
    )


def provider_view(request):
    return render(request, "analyzers/provider.html")


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