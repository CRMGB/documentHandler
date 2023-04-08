import typing
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import NewUserForm

RedirectOrResponse = typing.Union[HttpResponseRedirect, HttpResponse]


def register(request: HttpRequest) -> RedirectOrResponse:
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("csv_upload")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request, "register.html", context={"register_form": form, "page": "register"}
    )


def login_request(request: HttpRequest) -> RedirectOrResponse:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("csv_upload")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request,
        template_name="login.html",
        context={"login_form": form, "page": "login"},
    )


def logout(request) -> HttpResponseRedirect:
    auth.logout(request)
    messages.success(request, f"You are now logged out")
    return redirect("register.html")
