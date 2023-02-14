from django.urls import path
from .views import UploadView
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('csv_upload', UploadView.as_view(), name="csv_upload"),
  path("csv_content/<str:pk>", views.csv_content, name="csv_content"),
]