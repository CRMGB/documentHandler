import uuid
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from .models import UploadCSVFileModel
from .forms import SimpleTable, UploadCSVFileForm, UploadCSVForm
from csv import DictReader
from io import TextIOWrapper
CRITICAL = 50

class UploadView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "csv_upload.html", {"form": UploadCSVFileForm()})

    def post(self, request):
        """ POST method to Handle the CSV upload, checks whether the id is unique,
            If there is not an error, save the content and display it in the csv_content template"""        
        csv_file = request.FILES["csv_file"]
        rows = TextIOWrapper(csv_file, encoding= "utf-8", newline="")
        row_count = 0
        for row in DictReader(rows):
            row_count += 1
            if is_valid_uuid(row.get("book_id"))==False:
                messages.add_message(request, CRITICAL, f"The book with the id '{row['book_id']}' is wrong.")
                return redirect("csv_upload")
            if UploadCSVFileModel.objects.filter(book_id=row.get("book_id")).exists():
                messages.add_message(request, CRITICAL, f"The book with the id '{row['book_id']}' is already present in the database.")
                return redirect("csv_upload")
            form = UploadCSVFileForm(row)
            if not form.is_valid():
                messages.add_message(request, CRITICAL, str(form.errors))
                return redirect("csv_upload")
            form.save()
        csv_content = UploadCSVFileModel.objects.order_by('-updated')
        table = SimpleTable(csv_content)
        context = {'table': table, "row_count": str(row_count)}
        return render(request, 'csv_content.html', context)


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False