from django.urls import path
from .views import UploadView
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('csv_upload', UploadView.as_view(), name="csv_upload"),

]