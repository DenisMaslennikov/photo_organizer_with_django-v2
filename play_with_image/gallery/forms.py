from django import forms

from image.models import Image
from tag_anything.models import TagCategory


class AssignTag(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=Image.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        empty_value="Введите тег",
        label="Тег",
    )
    category = forms.ModelChoiceField(
        queryset=TagCategory.objects.all(),
        label="Категория",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
