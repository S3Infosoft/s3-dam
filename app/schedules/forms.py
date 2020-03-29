from .models import Schedule
from django import forms
from django.utils.timezone import now


class ScheduleHandlingForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = "ota_name", "check_in_date", "check_out_date",
        widgets = {
            "check_in_date": forms.DateInput(attrs={
                "class": "form-control datepicker",
                "data-provide": "datepicker",
                "placeholder": "mm/dd/yyyy",
                "min": now().date()
            }),
            "check_out_date": forms.DateInput(attrs={
                "class": "form-control datepicker",
                "data-provide": "datepicker",
                "placeholder": "mm/dd/yyyy",
                "min": now().date()
            })
        }

    def __init__(self, *args, **kwargs):
        super(ScheduleHandlingForm, self).__init__(*args, **kwargs)
        self.fields["ota_name"].widget.attrs = {"class": "form-control"}
