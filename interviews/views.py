from django.http import HttpResponseNotAllowed

from django.shortcuts import render, get_object_or_404, redirect

from jobs.models import Job

from .models import Chat


def create(request, job_pk):
    if request.method == "POST":
        job = get_object_or_404(Job, pk=job_pk)
        Chat.objects.create(job=job)
        return redirect ("jobs:details", {"pk": job_pk})
    return HttpResponseNotAllowed(permitted_method=("POST", ))
