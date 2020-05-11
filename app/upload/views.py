from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from photologue.forms import UploadZipForm
from .mayan import documentUpload, documentView


def uploadPhoto(request):
    if request.method == "POST":
        imageform = PhotoUploadForm(request.POST or None, request.FILES or None)
        zipform = UploadZipForm(request.POST or None, request.FILES or None)
        # to save single image
        if imageform.is_valid():
            imageform.save()
            messages.success(request, "photos uploaded")
        # to save a zip of image
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
        responce = documentUpload(request)
        print(responce)
        # create a document object
        Document.objects.create(
            description=responce["description"],
            document_type=responce["document_type"],
            document_id=responce["id"],
            label=responce["label"],
            language=responce["language"],
        )
        messages.success(request, "document uploaded")
        return redirect("uploadDocument")

    form = documentForm()
    data = {"title": "upload document", "documentForm": form}
    return render(request, "upload/uploadDocument.html", data)


def viewDocument(request):
    responce = documentView()
