from django.urls import path
from .views import DisplayCSVRowsListView, UploadView

urlpatterns = [
    path("csv_upload", UploadView.as_view(), name="csv_upload"),
    path("csv_content/<str:pk>", DisplayCSVRowsListView.as_view(), name="csv_content"),
]
