from django.urls import path

from .views import list_jobs

app_name = "jobs"
urlpatterns = [
    path('', list_jobs, name="list")
]