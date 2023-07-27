from datetime import date, timedelta

from django import forms
from django.core.exceptions import ValidationError


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
