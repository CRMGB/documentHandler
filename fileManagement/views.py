import typing as t
import uuid
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import Any
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.base import View
from .aws_s3 import upload_csv_to_s3
from .models import UploadCSVFileModel
from .forms import SimpleTable, UploadCSVFileForm
from csv import DictReader
from io import TextIOWrapper
CRITICAL = 50

RedirectOrResponse = t.Union[HttpResponseRedirect, HttpResponse]

class UploadView(View):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any)-> HttpResponse:
        return render(request, "csv_upload.html", {"form": UploadCSVFileForm()})

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any)-> RedirectOrResponse:
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
        upload_csv_to_s3(csv_file, row_count)
        csv_content = UploadCSVFileModel.objects.order_by('-updated')
        table = SimpleTable(csv_content)
        context = {'table': table, "row_count": str(row_count)}
        return render(request, 'csv_content.html', context)


def is_valid_uuid(val: uuid)->bool:
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False