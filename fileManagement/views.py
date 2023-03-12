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
from .forms import CSVFileRowsForm, SimpleTable
from csv import DictReader
from io import TextIOWrapper
from django.core.paginator import Paginator

RedirectOrResponse = typing.Union[HttpResponseRedirect, HttpResponse]

class UploadView(View):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any)-> HttpResponse:
        """Display the upload template and display the files saved for the logged user."""
        files = CSVFileModel.objects.filter(user__id=self.request.user.id)
        paginator = Paginator(files, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {"form": CSVFileRowsForm(), "page_obj": page_obj, 'files':files}
        return render(request, "csv_upload.html", context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any)-> RedirectOrResponse:
        """ POST method to Handle the CSV upload, checks whether the id is unique,
            If there is not an error, save the content and display it in the csv_content template"""        
        
        csv_file = request.FILES.get("csv_file")
        rows = TextIOWrapper(csv_file, encoding="utf-8", newline="")
        form_rows:list = []
        row_count:int = 0
        for row in DictReader(rows):
            row_count += 1
            if CSVRowsModel.objects.filter(book_id=row.get("book_id")).exists():
                messages.error(request, f"The book with the id '{row['book_id']}' is already present in the database.")
                return redirect("csv_upload")
            if not is_valid_uuid(row.get("book_id")):
                messages.error(request, f"The book with the id '{row['book_id']}' is wrong.")
                return redirect("csv_upload")
            form = CSVFileRowsForm(row)
            if not form.is_valid():
                messages.error(request, str(form.errors))
                return redirect("csv_upload")
            form = form.save(commit=False)
            form.save()
            form_rows.append(form)
        table = self.create_file_and_send_to_s3(row_count, csv_file, form_rows)
        context = {'table': table, "row_count": str(row_count)}
        return render(request, 'csv_content.html', context)

    def create_file_and_send_to_s3(self, row_count: int, csv_file:HttpRequest, form_rows: list)-> SimpleTable:
        """ Create the File instance after the rows have been validated and saved,
        also make the fk association, send to s3 and display in django_tables2"""
        file_model = CSVFileModel.objects.create(
            file_name=csv_file.name, 
            user=self.request.user,
            row_count=row_count
        )
        for row in form_rows:
            row.file = file_model
            row.save()      
        upload_csv_to_s3(csv_file, row_count)
        csv_content = CSVRowsModel.objects.filter(file=file_model)
        return SimpleTable(csv_content)

def csv_content(request, pk):
    """Display the csv selected on a table."""
    if csv := CSVRowsModel.objects.filter(file__id=pk):
        table = SimpleTable(csv)
        table.paginate(page=request.GET.get("page", 1), per_page=10)
        context = {'table': table}
        return render(request, 'csv_content.html', context)
    messages.error(request, f"The file with the id '{pk}' hasn't been found.")


def is_valid_uuid(val: uuid)->bool:
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False