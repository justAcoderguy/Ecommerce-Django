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
    # is_active is set as default to True, so its not needed in Factory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    # Parameters
    web_id = factory.Sequence(lambda n : "web_id_%d" % n),
    slug = fake.lexify(text="prod_slug_???????"),
    name = fake.lexify(text="prod_name_???????"),
    description = fake.text(),
    created_at = "2022-06-23 13:40:13.279092",
    updated_at = "2022-06-23 13:40:13.279092"

     # https://factoryboy.readthedocs.io/en/stable/reference.html?highlight=PostGeneration#factory.post_generation
    @factory.post_generation
    # Name of function should be name of parameter passed in create()
    def category(self, create, extracted, **kwargs):
        if not create or not extracted:
            return 
        
        if extracted:
            for cat in extracted:
                self.category.add(cat)


register(CategoryFactory)
register(ProductFactory)



