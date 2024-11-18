from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Driver, Car


class LicenseValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise forms.ValidationError("Length of license number must be 8")
        if not (license_number[:3].isalpha() and license_number[:3].isupper()):
            raise forms.ValidationError(
                "License number must start with 3 uppercase letters"
            )
        if not (license_number[3:].isnumeric()):
            raise forms.ValidationError(
                "License number must end with 5 digits"
            )
        return license_number


class DriverCreationForm(UserCreationForm,
                         LicenseValidationMixin):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name",
                                                 "last_name",
                                                 "license_number", )


class DriverLicenseUpdateForm(forms.ModelForm,
                              LicenseValidationMixin):
    class Meta:
        model = Driver
        fields = ("license_number", )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = "__all__"
