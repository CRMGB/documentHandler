import typing
import uuid
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import Any
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.base import View
from .aws_s3 import upload_csv_to_s3
from .models import CSVFileModel, CSVRowsModel
from .forms import CSVFileForm, CSVFileRowsForm, SimpleTable
from csv import DictReader
from io import TextIOWrapper

RedirectOrResponse = typing.Union[HttpResponseRedirect, HttpResponse]

class UploadView(View):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any)-> HttpResponse:
        """Display the upload template and display the files saved for the logged user."""
        files = CSVFileModel.objects.filter(user__id=self.request.user.id)
        context = {"form": CSVFileRowsForm(), "files": files}
        return render(request, "csv_upload.html", context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any)-> RedirectOrResponse:
        """ POST method to Handle the CSV upload, checks whether the id is unique,
            If there is not an error, save the content and display it in the csv_content template"""        
        
        csv_file = request.FILES["csv_file"]
        rows = TextIOWrapper(csv_file, encoding= "utf-8", newline="")
        file_model = CSVFileModel.objects.create(
            file_name=request.FILES["csv_file"].name, 
            user=self.request.user
        )
        row_count = 0
        for row in DictReader(rows):
            row_count += 1
            if CSVRowsModel.objects.filter(book_id=row.get("book_id")).exists():
                messages.error(request, f"The book with the id '{row['book_id']}' is already present in the database.")
                file_model.delete()
                return redirect("csv_upload")
            if is_valid_uuid(row.get("book_id"))==False:
                messages.error(request, f"The book with the id '{row['book_id']}' is wrong.")
                return redirect("csv_upload")
            form = CSVFileRowsForm(row)
            if not form.is_valid():
                messages.error(request, str(form.errors))
                return redirect("csv_upload")
            form = form.save(commit=False)
            form.file = file_model
            form.save()
        upload_csv_to_s3(csv_file, row_count)
        CSVFileModel.objects.filter(id=file_model.id).update(row_count=row_count)
        csv_content = CSVRowsModel.objects.filter(file=file_model)
        table = SimpleTable(csv_content)
        context = {'table': table, "row_count": str(row_count)}
        return render(request, 'csv_content.html', context)


def csv_content(request, pk):
    """Display the csv selected on a table."""
    if csv := CSVRowsModel.objects.filter(file__id=pk):
        table = SimpleTable(csv)
        context = {'table': table}
        return render(request, 'csv_content.html', context)
    messages.error(request, f"The file with the id '{pk}' hasn't been found.")


def is_valid_uuid(val: uuid)->bool:
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False