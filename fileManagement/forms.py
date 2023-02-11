from django.forms import FileField, Form, ModelForm
from .models import UploadCSVFileModel


class UploadCSVFileForm(ModelForm):
    class Meta:
        model = UploadCSVFileModel
        fields = ["book_title", "book_author", "date_published", "book_id", "publisher_name"]

class UploadCSVForm(Form):
    csv_file = FileField()
    # id = forms.UUIDField()
