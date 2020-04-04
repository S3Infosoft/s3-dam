from photologue.models import Photo


from django import forms


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'