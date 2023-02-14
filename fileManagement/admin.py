from django.contrib import admin

from .models import CSVRowsModel, CSVFileModel

admin.site.register(CSVRowsModel)

admin.site.register(CSVFileModel)
