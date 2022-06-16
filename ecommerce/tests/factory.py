from statistics import mode
from faker import Faker
import pytest
import factory
from faker import Faker
from pytest_factoryboy import register

fake = Faker()

from inventory import models

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    # Parameters
    name = fake.lexify(text="cat_name_???????")
    slug = fake.lexify(text="cat_slug_???????")

register(CategoryFactory)
