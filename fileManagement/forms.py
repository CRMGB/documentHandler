from django.urls import reverse
import django_tables2 as tables
from django.forms import FileField, Form, ModelForm
from .models import CSVFileModel, CSVRowsModel
from django_filters import FilterSet
from django_tables2.utils import A
from django.utils.safestring import mark_safe


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


class TableFileCSV(tables.Table):
    view = tables.LinkColumn('csv_content', args=[A('pk')], orderable=False, empty_values=())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created = tables.DateTimeColumn(format ='d M Y, h:i A')
        self.updated = tables.DateTimeColumn(format ='d M Y, h:i A')

    class Meta:
        model = CSVFileModel
        attrs = {
            "class": "table table-striped table-hover dt-responsive nowrap",
        }
        exclude = ["id", "user"]
        order_by = 'updated'

    def render_view(self):
        return 'Display'
    
class TableRowsFileFilter(FilterSet):
    class Meta:
        model = CSVFileModel
        fields = {"file_name": ["contains"], "created": ["contains"]}

class TableRowsCSV(tables.Table):

    def __init__(self, *args, overriden_value="",**kwargs):
        super().__init__(*args, **kwargs)
        self.base_columns['book_author'].verbose_name = "Author"
        self.base_columns['publisher_name'].verbose_name = "Publisher"
        self.created = tables.DateTimeColumn(format ='d M Y, h:i A')
        self.updated = tables.DateTimeColumn(format ='d M Y, h:i A')            

    class Meta:
        model = CSVRowsModel
        attrs = {
            "class": "table table-striped table-hover dt-responsive nowrap",
        }
        exclude = ["id", "file"]
        order_by = 'updated'


class TableRowsCSVFilter(FilterSet):
    class Meta:
        model = CSVRowsModel
        fields = {"book_title": ["contains"], "book_author": ["contains"]}