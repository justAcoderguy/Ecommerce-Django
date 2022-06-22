from statistics import mode
from faker import Faker
import pytest
import factory
from faker import Faker
from pytest_factoryboy import register

fake = Faker()

from inventory import models

# Factory - https://factoryboy.readthedocs.io/en/stable/orms.html
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    # Parameters - This will not provide unique names / slug
    # name = fake.lexify(text="cat_name_???????")
    # slug = fake.lexify(text="cat_slug_???????")

    # Paramters - For unique constraint to be upheld
    name = factory.Sequence(lambda n : "cat_name_%d" % n)
    slug = factory.Sequence(lambda n : "cat_slug_%d" % n)

register(CategoryFactory)
