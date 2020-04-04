from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from .forms import PhotoUploadForm
from photologue.forms import UploadZipForm


def uploadPhoto(request):
    if request.method == "POST":

        imageform = PhotoUploadForm(request.POST or None)
        zipform = UploadZipForm(request.POST or None)
        
        if imageform.is_valid():
            imageform.save()
        if zipform.is_valid():
            zipform.save()

        messages.success(request,'photos uploaded')
        return redirect('uploadPhoto')

    imageform = PhotoUploadForm()
    zipform = UploadZipForm()
    data = {
        'title':'upload image',
        'imageform':imageform,
        'zipform':zipform,
    }
    return render(request,'upload/uploadPhoto.html',data)

def uploadDocument(request):
    if request.method == 'post':
        pass
    data={
        'title':'upload document',
    }
    return render(request,'upload/uploadDocument.html',data)