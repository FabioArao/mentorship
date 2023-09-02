from django.urls import path

from .views import create

app_name = "interviews"
urlpatterns = [
    path("create/<int:job_pk>", create, name="create")
]