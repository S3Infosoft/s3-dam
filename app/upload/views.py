import socket
import requests
import os
from django.shortcuts import render, redirect
from django.contrib import messages

from django.conf import settings
from django.core.files.storage import FileSystemStorage


#### for photologue #######################
from .forms import *
from photologue.forms import UploadZipForm

###########################################

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


def uploadPhoto(request):
    if request.method == "POST":
        imageform = PhotoUploadForm(request.POST or None, request.FILES or None)
        zipform = UploadZipForm(request.POST or None, request.FILES or None)
        if imageform.is_valid():
            imageform.save()
            messages.success(request, "photos uploaded")
        if zipform.is_valid():
            zipform.save()
            messages.success(request, "zip of photos uploaded")
        return redirect("uploadPhoto")
    imageform = PhotoUploadForm()
    zipform = UploadZipForm()
    data = {"title": "upload image", "imageform": imageform, "zipform": zipform}
    return render(request, "upload/uploadPhoto.html", data)


def uploadDocument(request):
    if request.method == "POST":
        return _document_upload(request)

    form = documentForm()
    data = {"title": "upload document", "documentForm": form}
    return render(request, "upload/uploadDocument.html", data)


def _document_upload(request):
    myfile = request.FILES["file"]
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    # api call
    ip = str("192.168.43.61")
    url = "http://" + ip + ":80/api/documents/"
    with open(".." + fs.path(filename), mode="rb") as file_object:
        document = requests.post(
            url,
            auth=("s3infosoft", "admin"),
            files={"file": file_object},
            data={"document_type": 1},
        ).json()
    print(document)
    #
    form = documentForm()
    data = {"title": "upload document", "documentForm": form}
    messages.success(request, "documentc uploaded")
    return render(request, "upload/uploadDocument.html", data)
