from django.forms import FileField, Form, ModelForm
from .models import UploadCSVFileModel
import django_tables2 as tables


class UploadCSVFileForm(ModelForm):
    class Meta:
        model = UploadCSVFileModel
        fields = ["book_title", "book_author", "date_published", "book_id", "publisher_name"]

class UploadCSVForm(Form):
    csv_file = FileField()


class SimpleTable(tables.Table):
    class Meta:
        model = UploadCSVFileModel
        attrs = {'class': 'table table-striped table-hover'}
        exclude = ["id"]
