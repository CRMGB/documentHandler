from django.contrib import messages
from django.shortcuts import render
from django.views.generic.base import View
from .models import UploadCSVFileModel
from .forms import SimpleTable, UploadCSVFileForm, UploadCSVForm
from csv import DictReader
from io import TextIOWrapper

CRITICAL = 50

class UploadView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "csv_upload.html", {"form": UploadCSVFileForm()})

    def post(self, request):
        csv_file = request.FILES["csv_file"]
        row_count = self.handle_cv_file(csv_file, request)
        csv_content = UploadCSVFileModel.objects.order_by('-updated')
        table = SimpleTable(csv_content)
        context = {'table': table, "row_count": str(row_count)}
        return render(request, 'csv_content.html', context)

    def handle_cv_file(self, csv_file, request):
        """ Separated method to Handle the CSV upload, checks whether the id is unique,
            If there is not an error, save the content and display it"""
        rows = TextIOWrapper(csv_file, encoding= "utf-8", newline="")
        row_count = 0
        for row in DictReader(rows):
            row_count += 1
            if UploadCSVFileModel.objects.filter(book_id=row.get("book_id")).exists():
                messages.add_message(request, CRITICAL, f"The book with the id {row['book_id']} is already present in the database.")
            form = UploadCSVFileForm(row)
            if not form.is_valid():
                messages.add_message(request, CRITICAL, str(form.errors))
            form.save()
        return row_count
