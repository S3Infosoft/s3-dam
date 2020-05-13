from django.db import models


class Document(models.Model):
    """
	this model save responce from
	mayan after uploading
	"""

    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=10, blank=True)
    document_id = models.IntegerField(blank=True)
    fileUrl = models.URLField(max_length=200, blank=True)
    downloadUrl = models.URLField(max_length=200, blank=True)
    previewUrl = models.URLField(max_length=200, blank=True)
    label = models.TextField(blank=True)
    language = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.label
