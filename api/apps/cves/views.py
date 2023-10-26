from django.shortcuts import render
from apps.cves.models import RedHatError
import json
import re
from concurrent.futures import ThreadPoolExecutor

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.views.generic import TemplateView

class ErrorTableView(TemplateView):
    template_name = 'cves/error_table_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_tables'] = None
        return context
    
@api_view(['POST'])
def error_table_api_view(request):
    # Get the input from the text box
    input_text = request.POST.get('input_text')
    # Extract the error codes from the input text
    pattern = r'CVE-\d{4}-\d{4,7}'
    error_codes = re.findall(pattern, input_text)
    # Get the error tables for the error codes using a ThreadPoolExecutor
    def get_error_table_wrapper(error_code):
        r, created = RedHatError.objects.get_or_create(error_code=error_code)
        return r.get_error_table()
    with ThreadPoolExecutor() as executor:
        error_tables = list(executor.map(get_error_table_wrapper, error_codes))
    # Render the error table template with the error tables
    html = render_to_string('cves/error_table.html', {'error_tables': error_tables})
    
    # Return the HTML response
    return Response({'html': html.strip()})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@api_view(['GET'])
def error_table_api_json(request):
    # Get the input from the text box
    input_text = request.GET.get('input_text')
    # Extract the error codes from the input text
    pattern = r'CVE-\d{4}-\d{4,7}'
    error_codes = re.findall(pattern, input_text)
    # Get the error tables for the error codes using a ThreadPoolExecutor
    def get_error_table_wrapper(error_code):
        r, created = RedHatError.objects.get_or_create(error_code=error_code)
        return r.get_error_table()
    with ThreadPoolExecutor() as executor:
        error_tables = list(executor.map(get_error_table_wrapper, error_codes))
    return Response({'data': error_tables})
