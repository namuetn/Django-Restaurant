from django import forms

from accounts.validators import allow_only_validator

from vendor.models import Vendor


class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
        validators=[allow_only_validator]  # Đặt validators ở đây
    )

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
