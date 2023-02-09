from django.shortcuts import render

# Create your views here.
def csv_upload(request):
    page = "csv_upload"
    number = 10
    context = {"page": page, "number": number}
    return render(request, "csv_upload.html", context)
