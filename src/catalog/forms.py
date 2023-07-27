from datetime import date, timedelta

from django import forms
from django.core.exceptions import ValidationError

from catalog.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Введите дату между сегодня + 4 недели (по-умолчанию 3).",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def clean_renewal_date(self):
        renewal_date = self.cleaned_data["renewal_date"]

        if renewal_date < date.today():
            raise ValidationError("Дата продления не может быть в прошлом.")

        if renewal_date > date.today() + timedelta(weeks=4):
            raise ValidationError("Продление больше, чем на 4 недели.")

        return renewal_date


class RenewBookModelForm(forms.ModelForm):
    def clean_due_back(self):
        renewal_date = self.cleaned_data["due_back"]

        if renewal_date < date.today():
            raise ValidationError("Дата продления не может быть в прошлом.")

        if renewal_date > date.today() + timedelta(weeks=4):
            raise ValidationError("Продление больше, чем на 4 недели.")

        return renewal_date

    class Meta:
        model = BookInstance
        fields = ("due_back",)
        labels = {"due_back": "Дата возврата"}
        widgets = {"due_back": forms.DateInput(attrs={"type": "date"})}
        help_texts = {"due_back": "Введите дату между сегодня + 4 недели (по-умолчанию 3)."}
