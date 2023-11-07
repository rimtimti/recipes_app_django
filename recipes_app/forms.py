from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea, TextInput, NumberInput
from recipes_app.models import Recipe, Category

from enum import Enum


class CategoryEnum(Enum):
    ITEM = ""


CATEGORY = ((CategoryEnum.ITEM.value, ""),)
CATEGORY = {
    (i[0], i[1][0])
    for i in enumerate(Category.objects.values_list("name").distinct(), 1)
}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.Select(
                attrs={"required": "True"},
                choices=(CATEGORY),
            ),
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description", "steps", "cooking_time", "image"]
        widgets = {
            "name": TextInput(attrs={"style": "width: 100%"}),
            "description": Textarea(attrs={"style": "width: 100%"}),
            "steps": Textarea(attrs={"style": "width: 100%"}),
            "cooking_time": NumberInput(attrs={"style": "width: 100%"}),
        }


class СookbookForm(forms.Form):
    name = forms.CharField(
        label="Название рецепта",
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите название",
                "required": "True",
            }
        ),
    )

    category = forms.CharField(
        label="Категория",
        required=False,
        widget=forms.Select(
            attrs={"required": "True"},
            choices=(CATEGORY),
        ),
    )

    description = forms.CharField(
        label="Описание рецепта",
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Введите описание",
                "required": "True",
            }
        ),
    )

    steps = forms.CharField(
        label="Этапы приготовления",
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Введите этапы приготовления",
                "required": "True",
            }
        ),
    )

    cooking_time = forms.IntegerField(
        min_value=0,
        label="Время приготовления",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control", "required": "True"}),
    )

    image = forms.ImageField(
        label="Фото готового блюда",
        required=False,
        widget=forms.FileInput(attrs={"required": "True"}),
    )


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", max_length=20)
    password = forms.CharField(
        label="Пароль", max_length=20, widget=forms.PasswordInput
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "Имя пользователя"}
