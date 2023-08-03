from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from Micro.products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "handle", "price"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "Enter Your Name"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["image", "name", "handle", "price"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "Enter Your Name"
        for field in self.fields:
            if field != "image":
                self.fields[field].widget.attrs["class"] = "form-control"

            self.fields[field].widget.attrs[
                "class"
            ] = "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
