from django.shortcuts import render
from .models import Job

def list_jobs(request):
    return render(request, "jobs/list.html", {"page_title": "Jobs List", "jobs":Job.objects.all()})
