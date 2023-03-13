from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.files.base import ContentFile
from csv_generator.forms import SchemaForm
from csv_generator.models import Schema, Datasets
from django.template.defaulttags import register

from csv_generator.utils import generate_csv


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_range_element(dictionary, index):
    return dictionary.get('range')[index]


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='/login/')
def schema_list(request):
    return render(request, 'schema_list.html', {'schemas': Schema.objects.all()})


@login_required(login_url='/login/')
def schema_update(request, pk):
    schema = get_object_or_404(Schema, pk=pk)
    if request.method == "POST":
        schema_name = request.POST.get('name')
        schema_separator = request.POST.get('separator')
        schema_str_char = request.POST.get('string_character')
        columns = get_columns(request.POST)
        schema.name = schema_name
        schema.separator = schema_separator
        schema.string_char = schema_str_char,
        schema.columns = columns
        schema.save()
    return render(request, 'schema_update.html', {'schema': schema,
                                                  'form': SchemaForm()})


@login_required(login_url='/login/')
def schema_detail(request, pk):
    data = get_object_or_404(Schema, pk=pk)
    if is_ajax(request):
        if request.method == "GET":
            pass
        if request.method == "POST":
            dataset = Datasets.objects.create(schema_id=pk, status='P')
            csv = generate_csv(data, request.POST)
            dataset.csv_file = ContentFile(csv, name=f'csv_{dataset.id}.csv')
            dataset.status = 'R'
            dataset.save()
            return JsonResponse({"url": dataset.csv_file.url})
    return render(request, 'schema_detail.html', {'schema': data, 'datasets': Datasets.objects.filter(schema_id=pk)})


def get_columns(POST):
    columns = []
    for column_data in filter(lambda s: s.startswith('column'), POST.keys()):
        if '_name' in column_data:
            pk = column_data.split('_')[1]
            column_name = POST.get(f'column_{pk}_name')
            column_type = POST.get(f'column_{pk}_type')
            column_range = POST.get(f'column_{pk}_range_from'), POST.get(
                f'column_{pk}_range_to')
            column_order = POST.get(f'column_{pk}_order')

            if column_type in ('int',) and not all(column_range):
                return JsonResponse({"error": "Spec"}, status=400)

            temp = {
                'name': column_name,
                'type': column_type,
                'order': column_order
            }
            if all(column_range):
                temp['range'] = column_range
            columns.append(temp)
    return columns


class SchemaCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, *args, **kwargs):
        return render(self.request, 'schema_create.html', {'form': SchemaForm()})

    def post(self, *args, **kwargs):
        schema_name = self.request.POST.get('name')
        schema_separator = self.request.POST.get('separator')
        schema_str_char = self.request.POST.get('string_character')
        columns = get_columns(self.request.POST)
        Schema.objects.create(user=self.request.user,
                              name=schema_name,
                              separator=schema_separator,
                              string_char=schema_str_char,
                              columns=columns)
        return redirect('schema_list')

    def delete(self, request, *args, **kwargs):
        schema_id = kwargs.get('pk')
        schema = get_object_or_404(Schema, pk=schema_id)

        if schema.user != request.user:
            return JsonResponse({"error": "You are not authorized to delete this schema."}, status=403)

        schema.delete()

        return JsonResponse({"success": "Schema deleted successfully."})
