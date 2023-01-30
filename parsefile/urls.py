from . import views
from django.urls import path

app_name = "parsefile"

urlpatterns = [
    path("", views.cnab_file, name = "cnab_file"),
]