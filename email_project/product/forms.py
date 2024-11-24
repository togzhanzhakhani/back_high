from django import forms
from .models import ProductDataset
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = ['csv']

def validate_file_extension(value):
    file_extension = value.name.split('.')[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Invalid file extension. Allowed extensions are: {', '.join(ALLOWED_EXTENSIONS)}.")
    return value


class ProductDatasetUploadForm(forms.ModelForm):
    class Meta:
        model = ProductDataset
        fields = ['file']
    file = forms.FileField(validators=[validate_file_extension])
