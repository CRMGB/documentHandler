import django_tables2 as tables
from django.forms import FileField, Form, ModelForm
from .models import CSVFileModel, CSVRowsModel
from django_filters import FilterSet


class CSVFileForm(ModelForm):
    class Meta:
        model = CSVFileModel
        fields = ["file_name"]

class CSVFileRowsForm(ModelForm):
    class Meta:
        model = CSVRowsModel
        fields = [
            "book_title", 
            "book_author", 
            "date_published", 
            "book_id", 
            "publisher_name",
            "updated",
        ]
        exclude = ["created", "updated"]

class UploadCSVForm(Form):
    csv_file = FileField()

class SimpleTable(tables.Table):
    created = tables.DateTimeColumn(format ='d M Y, h:i A')
    updated = tables.DateTimeColumn(format ='d M Y, h:i A')

    class Meta:
        model = CSVRowsModel
        attrs = {
            'class': 'table table-striped table-hover',
            "thead": {"class": "thead-dark"}
        }
        exclude = ["id"]
        order_by = 'updated'


class CSVTableFilter(FilterSet):
    class Meta:
        model = CSVRowsModel
        fields = {"book_title": ["contains"], "book_author": ["contains"]}