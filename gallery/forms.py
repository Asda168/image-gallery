from django import forms

from .models import Photo


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["title", "description", "image", "category", "photographer"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Give your photo a title"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Tell its story (optional)"}),
            "photographer": forms.TextInput(attrs={"placeholder": "Your name (optional)"}),
        }
