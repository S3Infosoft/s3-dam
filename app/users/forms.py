from . import models

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreateForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = "email",


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = "email",


class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = "email", "first_name", "last_name",

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields["first_name"].required = True


class GlobalInfoAdminForm(forms.ModelForm):
    class Meta:
        model = models.GlobalInfo
        fields = "__all__"
        widgets = {"address": forms.Textarea()}


class GlobalInfoForm(forms.ModelForm):
    clear = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        "class": "form-check-input"
    }), required=False)

    class Meta:
        model = models.GlobalInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(GlobalInfoForm, self).__init__(*args, **kwargs)
        self.fields["logo"].widget.attrs = {"class": "custom-file-input"}
        self.fields["address"].widget = forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Your address",
            "maxlength": 350,
            "style": "height: 150px"
        })

    def save(self, commit=True):
        user_info = super(GlobalInfoForm, self).save(commit=False)

        if self.cleaned_data["clear"]:
            user_info.logo.delete(save=False)

        if commit:
            user_info.save()

        return user_info
