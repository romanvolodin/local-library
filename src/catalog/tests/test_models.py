from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog.models import Author


class TestAuthorModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(
            first_name="Имя1",
            last_name="Фамилия1",
        )
        Author.objects.create(
            first_name="Имя2",
            last_name="Фамилия2",
            date_of_birth="2000-01-01",
            date_of_death="2000-01-01",
        )
        Author.objects.create(
            first_name="Имя3",
            last_name="Фамилия3",
            date_of_birth="2000-01-01",
            date_of_death="1900-01-01",
        )

    def test_verbose_name(self):
        FIELD_VERBOSE_NAMES = {
            "first_name": "имя",
            "last_name": "фамилия",
            "date_of_birth": "дата рождения",
            "date_of_death": "дата смерти",
        }
        author = Author.objects.get(id=1)
        for field, expected_value in FIELD_VERBOSE_NAMES.items():
            with self.subTest(field=field):
                self.assertEqual(expected_value, author._meta.get_field(field).verbose_name)

    def test_str_representation(self):
        author = Author.objects.get(id=1)
        self.assertEquals(f"{author.last_name}, {author.first_name}", str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), "/catalog/authors/1/")

    def test_death_date_validation(self):
        author = Author.objects.get(id=2)
        self.assertRaises(ValidationError, author.clean)

    def test_death_date_validation_message_birth_should_not_be_equal_death(self):
        author = Author.objects.get(id=2)
        with self.assertRaisesMessage(
            ValidationError, "Дата смерти должна быть позже даты рождения"
        ):
            author.clean()

    def test_death_date_validation_message_death_should_be_after_birth(self):
        author = Author.objects.get(id=3)
        with self.assertRaisesMessage(
            ValidationError, "Дата смерти должна быть позже даты рождения"
        ):
            author.clean()
