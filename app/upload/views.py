from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import requests
from django.contrib import messages


def upload(request):
    if request.method == 'POST':
        try :
            file = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            with open(filename, mode='rb') as file_object:
                requests.post('http://localhost:8000/api/documents/', auth=('admin',
                                                                        '5YxqGjPLLk'), files={'file': file_object}, data={'document_type': 1}).json()

        except:
             messages.info(
                request, f"error occur, please try again"
            )

        data = {
            'title': 'upload'
        }

        return render(request, "upload/upload.html", data)

    data = {
        'title': 'upload'
    }

    return render(request, "upload/upload.html", data)
