import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.forms import AuthorForm, RenewBookModelForm
from catalog.models import Author, Book, BookInstance, Genre


User = get_user_model()


class RenewBookFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("Librarian", "lib@test.com", "passwd123")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        author = Author.objects.create(
            first_name="Имя",
            last_name="Фамилия",
        )
        genre = Genre.objects.create(name="Жанр")
        book = Book.objects.create(
            title="Название книги",
            author=author,
            summary="Краткое описание книги",
            isbn=1234567890123,
        )
        genre.books.add(book)
        self.book_instance = BookInstance.objects.create(
            book=book,
            imprint="Издание",
        )

    def test_renew_date_field_label(self):
        form = RenewBookModelForm()
        self.assertTrue(
            form.fields["due_back"].label is None
            or form.fields["due_back"].label == "Дата возврата"
        )

    def test_renew_date_field_help_text(self):
        form = RenewBookModelForm()
        self.assertEqual(
            form.fields["due_back"].help_text,
            "Введите дату между сегодня + 4 недели (по-умолчанию 3).",
        )

    def test_renew_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {"due_back": date}
        form = RenewBookModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form_data = {"due_back": date}
        form = RenewBookModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_message_renew_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form_data = {"due_back": date}
        url = reverse("renew-book-librarian", args=[self.book_instance.id])
        response = self.authorized_client.post(url, data=form_data, follow=True)
        self.assertFormError(
            response,
            "form",
            "due_back",
            "Продление больше, чем на 4 недели.",
        )

    def test_message_renew_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {"due_back": date}
        url = reverse("renew-book-librarian", args=[self.book_instance.id])
        response = self.authorized_client.post(url, data=form_data, follow=True)
        self.assertFormError(
            response,
            "form",
            "due_back",
            "Дата продления не может быть в прошлом.",
        )

    def test_renew_date_today(self):
        date = datetime.date.today()
        form_data = {"due_back": date}
        form = RenewBookModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form_data = {"due_back": date}
        form = RenewBookModelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_date_label(self):
        form = RenewBookModelForm()
        self.assertEqual("Дата возврата", form.fields["due_back"].label)

    def test_renew_date_help_text(self):
        form = RenewBookModelForm()
        self.assertEqual(
            "Введите дату между сегодня + 4 недели (по-умолчанию 3).",
            form.fields["due_back"].help_text,
        )


class AuthorFormTest(SimpleTestCase):
    def test_date_of_birth_widget_is_date(self):
        form = AuthorForm()
        self.assertEqual("date", form.fields["date_of_birth"].widget.input_type)

    def test_date_of_death_widget_is_date(self):
        form = AuthorForm()
        self.assertEqual("date", form.fields["date_of_death"].widget.input_type)
