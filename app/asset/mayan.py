import requests
import os
import json
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
    response["url"] = getDocumentUrl(response["id"])
    response["downloadUrl"] = getDocumentDownloadUrl(response["id"])
    response["previewUrl"] = getPreviewUrl(response["id"])
    return response


def getPreviewUrl(id):
    """
    function takes in id and return
    1st page img url of document
    """
    url = mayanFileUploadUrl + str(id) + "/versions/" + str(id) + "/pages/"
    response = requests.get(url, auth=(mayanUserName, mayanPassword)).json()
    response = response["results"][0]["image_url"]
    print(response)
    response = response.split("/")[3:]
    response = "/".join(response)
    response = "http://localhost/" + response
    return response


def getDocumentUrl(id):
    """
    function takes id
    and return formatted document url
    """
    return "http://localhost/" + str(id) + "/"


def getDocumentDownloadUrl(id):
    """
    function takes id
    and return formatted document download url
    """
    return "http://localhost/" + str(id) + "/versions/" + str(id) + "/download/"
