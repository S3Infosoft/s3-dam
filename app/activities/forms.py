from django import forms

DATE_FORMAT = "%d/%m/%Y"


class ReportEmailForm(forms.Form):
    subject = forms.CharField(max_length=250,
                              widget=forms.TextInput(
                                  attrs={"class": "form-control"}
                              ))
    message = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control"}
    ))
    to = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control"})
    )


class ReportForm(forms.Form):
    ENQUIRIES = (
        ("OTA", "OTA"),
        ("PARTNER", "Partner"),
        ("REVIEW", "Review"),
    )

    start_date = forms.DateField(widget=forms.DateInput(
        attrs={
            "class": "form-control datepicker",
            "data-provide": "datepicker",
            "placeholder": "mm/dd/yyyy",
        },
    ))
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={
            "class": "form-control datepicker",
            "data-provide": "datepicker",
            "placeholder": "mm/dd/yyyy",
        },
    ))
    enquiry_type = forms.ChoiceField(choices=ENQUIRIES, widget=forms.Select(
        attrs={"class": "form-control"}
    ))
