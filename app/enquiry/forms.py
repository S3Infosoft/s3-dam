from . import models
from django import forms


class OTAForm(forms.ModelForm):
    class Meta:
        model = models.OTA
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(OTAForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Name"
        }
        self.fields["contact_person"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Contact Person"
        }
        self.fields["contact_number"].widget.attrs = {
            "pattern": "\\d{10,15}",
            "class": "form-control",
            "placeholder": "Enter Contact Number"
        }
        self.fields["contact_email"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Contact Email",
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = models.Partner
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Name"
        }
        self.fields["partner_type"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Partner Type"
        }
        self.fields["contact_person"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Contact Person"
        }
        self.fields["contact_number"].widget.attrs = {
            "pattern": "\\d{10,15}",
            "class": "form-control",
            "placeholder": "Enter Contact Number"
        }
        self.fields["contact_email"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Contact Email",
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["headline"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Headline"
        }
        self.fields["source"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Source"
        }

        self.fields["rating"].widget.attrs = {
            "class": "form-control",
        }

        self.fields["description"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Description",
            "rows": 4,
        }

        self.fields["action"].widget.attrs = {
            "class": "form-control",
            "placeholder": "Enter Action",
            "rows": 4,
        }
