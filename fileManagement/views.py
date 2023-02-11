from django.shortcuts import render
from django.views.generic.base import View

from .models import UploadCSVFileModel
from .forms import UploadCSVFileForm, UploadCSVForm
from csv import DictReader
from io import TextIOWrapper

class UploadView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "csv_upload.html", {"form": UploadCSVFileForm()})

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES["csv_file"]
        row_count = self.handle_cv_file(csv_file, request)
        csv_content = UploadCSVFileModel.objects.order_by('-updated')
        return self.display_csv_on_table(request, csv_content, row_count)

    def handle_cv_file(self, csv_file, request):
        """ Separated method to Handle the CSV upload, checks whether the id is unique."""
        rows = TextIOWrapper(csv_file, encoding= "utf-8", newline="")
        row_count = 0
        for row in DictReader(rows):
            row_count += 1
            #str(uuid.uuid4())
            if UploadCSVFileModel.objects.filter(book_id=row["book_id"]).exists():
                return render(
                    request,
                    "csv_content.html",
                    {
                        "form": UploadCSVForm(), 
                        "form_errors": f"The book with the id {row['book_id']} is already present in the database."
                    }
                )                
            form = UploadCSVFileForm(row)
            if not form.is_valid():
                return render(
                    request,
                    "csv_content.html",
                    {"form": UploadCSVForm(), "form_errors": form.errors}
                )
            form.save()
        return row_count

    def display_csv_on_table(self, request, csv_content, row_count):
        fields= [
            field for field in UploadCSVFileModel._meta.get_fields() 
            if field.name != 'id'
        ]
        context = {'data' : csv_content, 'headers' : fields, "row_count": str(row_count)}
        return render(request, 'csv_content.html', context)