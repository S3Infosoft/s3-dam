import requests
from django.shortcuts import render, redirect
from django.contrib import messages

from django.conf import settings
from django.core.files.storage import FileSystemStorage


#### for photologue #######################
from .forms import *
from photologue.forms import UploadZipForm
###########################################


def uploadPhoto(request):
    if request.method == "POST":
        imageform = PhotoUploadForm(
            request.POST or None, request.FILES or None)
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
    data = {
        "title": "upload image",
        "imageform": imageform,
        "zipform": zipform,
    }
    return render(request, "upload/uploadPhoto.html", data)


def uploadDocument(request):
    # if request.method == "POST":
    #       return _document_upload(request)

    # form = DocumentUpladForm()
    data = {
        "title": "upload document",
        # "form":form,
    }
    return render(request, "upload/uploadDocument.html", data)


# def _document_upload(request):
#     myfile = request.FILES['file']
#     fs = FileSystemStorage()
#     filename = fs.save(myfile.name, myfile)
#     uploaded_file_url = settings.BASE_DIR + fs.url(filename)
#     print(filename,'  ',uploaded_file_url)
#     with open(uploaded_file_url, mode='rb') as file_object:
#         document = requests.post('http://127.0.0.1:80/api/documents/', auth=('admin', 'g34ntRyuh9'), files={'file': file_object}, data={'document_type': 1}).json()
#     print(document)
#     return render(request, "upload/uploadDocument.html", data)
