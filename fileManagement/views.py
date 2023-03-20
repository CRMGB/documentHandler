import typing
import uuid
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import Any
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from .aws_s3 import upload_csv_to_s3
from .models import CSVFileModel, CSVRowsModel
from .forms import CSVFileRowsForm, SimpleTable, CSVTableFilter
from django_tables2 import SingleTableView
from csv import DictReader
from io import TextIOWrapper
from django.core.paginator import Paginator
from django.views.generic import ListView

RedirectOrResponse = typing.Union[HttpResponseRedirect, HttpResponse]

class UploadView(ListView):
    paginate_by = 1
    model = CSVFileModel
    template_name = "csv_upload.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any)-> HttpResponse:
        """Display the upload template and display the files saved for the logged user."""
        try:
            files = CSVFileModel.objects.filter(user__id=self.request.user.id)
            paginator = Paginator(files, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {"form": CSVFileRowsForm(), "page_obj": page_obj, 'files':files}
            return render(request, "csv_upload.html", context)
        except AttributeError as error:
            messages.error(request, f"Something bad happened! {error}")

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any)-> HttpResponseRedirect:
        """ POST method to Handle the CSV upload, checks whether the id is unique,
            If there is not an error, save the content and display it in the csv_content template"""        
        
        form_rows:list = []
        row_count:int = 0
        try:
            csv_file = request.FILES.get("csv_file")
            rows = TextIOWrapper(csv_file, encoding="utf-8", newline="")
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
            file = self.create_file_and_send_to_s3(row_count, csv_file, form_rows)
            return redirect(f"csv_content/{file.id}")
        except AttributeError as error:
            messages.error(request, f"Something bad happened! {error}")

    def create_file_and_send_to_s3(self, row_count: int, csv_file:HttpRequest, form_rows: list)-> SimpleTable:
        """ send the file to s3, create the File instance after the rows have been validated and saved,
        also make the fk association,  and display in django_tables2"""
        file_name_s3 = upload_csv_to_s3(csv_file, row_count)
        file_model = CSVFileModel.objects.create(
            file_name=csv_file.name, 
            user=self.request.user,
            row_count=row_count,
            file_aws_s3_name=file_name_s3
        )
        for row in form_rows:
            row.file = file_model
            row.save()
        return file_model

class PagedFilteredTableView(SingleTableView):
    """ Standard Viewset to paginate and filter the table but we select the file entry by:
    get_queryset().filter(file__id=self.kwargs['pk'])"""
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        id = self.kwargs.get('pk')
        if CSVRowsModel.objects.filter(file__id=id):
            qs = super(PagedFilteredTableView, self).get_queryset().filter(file__id=self.kwargs['pk'])
            self.filter = self.filter_class(self.request.GET, queryset=qs)
            return self.filter.qs
        messages.error(self.request, f"The file with the id '{id}' hasn't been found.")

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data(**kwargs)
        context[self.context_filter_name] = self.filter
        return context

class DisplayCSVRowsListView(PagedFilteredTableView):
    """ This is the ViewSet called from the URLs and inheriting PagedFilteredTableView 
    which will do all the work for us."""
    table_class = SimpleTable
    model = CSVRowsModel
    paginate_by = 5
    template_name = "csv_content.html"
    filter_class = CSVTableFilter

def is_valid_uuid(val: uuid)->bool:
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False