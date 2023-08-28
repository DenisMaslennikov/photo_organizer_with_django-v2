from django import forms

from .models import Image
from .utils import get_average_image_hash


class ImageAddForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["name", "image", "tags", "private"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control rounded-0"}),
            "image": forms.FileInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

    def save(self, commit=True):
        image_hash = str(get_average_image_hash(self.cleaned_data["image"]))

        image = Image(
            image=self.cleaned_data["image"],
            name=self.cleaned_data["name"],
            private=self.cleaned_data["private"],
            image_hash=image_hash,
            image_hash_part1=int(image_hash[:4], 16),
            image_hash_part2=int(image_hash[4:8], 16),
            image_hash_part3=int(image_hash[8:12], 16),
            image_hash_part4=int(image_hash[12:16], 16),
            author=self.instance.author,
        )
        if commit:
            image.save()
            image.tags.add(*self.cleaned_data["tags"])
        return image


class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("name", "tags", "private")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control rounded-0"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
