from django.forms import FileField, Form, ModelForm
from .models import CSVFileModel, CSVRowsModel
import django_tables2 as tables


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
        ]

class UploadCSVForm(Form):
    csv_file = FileField()

class SimpleTable(tables.Table):
    class Meta:
        model = CSVRowsModel
        attrs = {'class': 'table table-striped table-hover'}
        exclude = ["id"]
