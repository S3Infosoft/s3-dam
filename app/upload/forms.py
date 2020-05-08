from photologue.models import Photo


from django import forms


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ("sites", "date_added")


class documentForm(forms.Form):
    description = forms.CharField(max_length=10)
    document_type = forms.CharField(max_length=10)
    file = forms.FileField()
    label = forms.CharField(max_length=10)
    language = forms.CharField(max_length=10)
