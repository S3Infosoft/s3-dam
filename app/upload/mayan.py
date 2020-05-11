import requests
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Document


ip = str("192.168.43.61")

# variables
mayanFileUploadUrl = "http://" + ip + ":80/api/documents/"
mayanUserName = "s3infosoft"
mayanPassword = "admin"


def documentUpload(request):
    """
	function to upload file to mayan sever
	this function takes request and save file and
	then upload
	"""
    File = request.FILES["file"]

    # file object
    fs = FileSystemStorage()
    fileName = fs.save(File.name, File)

    with open(".." + fs.path(fileName), mode="rb") as file_object:
        response = requests.post(
            mayanFileUploadUrl,
            auth=(mayanUserName, mayanPassword),
            files={"file": file_object},
            data={"document_type": 1},
        ).json()

    return response


def documentView():
    pass
    """
    function to get all document
    from mayan
    """
    # document = Document.objects.all()
    # for id in
