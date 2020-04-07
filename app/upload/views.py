import requests
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .forms import PhotoUploadForm
from photologue.forms import UploadZipForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage



def uploadPhoto(request):
    if request.method == "POST":

        imageform = PhotoUploadForm(request.POST or None)
        zipform = UploadZipForm(request.POST or None)

        if imageform.is_valid():
            instance = imageform.save(commit=False)
            instance.user = request.user
            instance.save()
        if zipform.is_valid():
            instance = zipform.save(commit=False)
            instance.user = request.user
            instance.save()


        messages.success(request, "photos uploaded")
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
    #     myfile = request.FILES['doc']
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
    #     uploaded_file_url = '..' + fs.url(filename)
    #     with open(uploaded_file_url, mode='rb') as file_object:
    #         document = requests.post('http://127.0.0.1/api/documents/', auth=('admin', 'wDp4a3UExK'), files={'file': file_object}, data={'document_type': 1}).json()
    #     print(document)

    data = {
        "title": "upload document",
    }
    return render(request, "upload/uploadDocument.html", data)
