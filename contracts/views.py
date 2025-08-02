import bleach
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
import jdatetime
from weasyprint import HTML
from .forms import ContractForm
from django.shortcuts import get_object_or_404
from .models import Contract

def pdf_template(request):
    return render(request, 'contracts/contract_template.html')

def admin_contract_pdf(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    contract.start_date = jdatetime.datetime.fromgregorian(
        datetime=contract.start_date).strftime("%Y/%m/%d")

    context_data = {
        "days": contract.duration_days,
        "amount": contract.total_amount
    }

    clean_clauses = []
    allowed_tags = getattr(settings, 'ALLOWED_HTML_TAGS', [])
    for clause in contract.clauses.all():
        clean_content = bleach.clean(clause.content, tags=allowed_tags)
        clean_clauses.append({
            "title": clause.title,
            "content": clean_content,
        })

    html = render_to_string(
        'contracts/contract_template.html',
        {'contract': contract, 'context_data': context_data, 'clauses': clean_clauses})

    pdf_file = HTML(
        string=html,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contract_{contract.employer.name}.pdf"'
    return response


def admin_contract_preview(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    contract.start_date = jdatetime.datetime.fromgregorian(
        datetime=contract.start_date).strftime("%Y/%m/%d")

    context_data = {
        "days": contract.duration_days,
        "amount": contract.total_amount
    }

    clean_clauses = []
    allowed_tags = getattr(settings, 'ALLOWED_HTML_TAGS', [])
    for clause in contract.clauses.all():
        clean_content = bleach.clean(clause.content, tags=allowed_tags)
        clean_clauses.append({
            "title": clause.title,
            "content": clean_content,
        })

    html = render_to_string(
        'contracts/local_contract_template_preview.html',
        {'contract': contract, 'context_data': context_data, 'clauses': clean_clauses})

    return HttpResponse(html)
