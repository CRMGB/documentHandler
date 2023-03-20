from django.forms import FileField, Form, ModelForm
from .models import CSVFileModel, CSVRowsModel

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
