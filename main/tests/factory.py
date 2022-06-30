from faker import Faker
import factory
from pytest_factoryboy import register
from inventory import models

fake = Faker()


# Factory - https://factoryboy.readthedocs.io/en/stable/orms.html
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    # Parameters - This will not provide unique names / slug
    # name = fake.lexify(text="cat_name_???????")
    # slug = fake.lexify(text="cat_slug_???????")

    # Paramters - For unique constraint to be upheld
    name = factory.Sequence(lambda n: "cat_name_%d" % n)
    slug = factory.Sequence(lambda n: "cat_slug_%d" % n)
    # is_active is set as default to True, so its not needed in Factory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    # Parameters
    web_id = factory.Sequence(lambda n: "web_id_%d" % n),
    slug = fake.lexify(text="prod_slug_???????"),
    name = fake.lexify(text="prod_name_???????"),
    description = fake.text(),
    created_at = "2022-06-23 13:40:13.279092",
    updated_at = "2022-06-23 13:40:13.279092"

    # https://factoryboy.readthedocs.io/en/stable/reference.html?highlight=PostGeneration#factory.post_generation
    """
        Many to Many relation between category and product implemented here.
        After product object is created, we add the category ids post object generation
        by using the 'category' parameter in the .create() function.
        Thats basically what happens in django behind the scenes if we inserted into the
        database
    """
    @factory.post_generation
    # Name of function should be name of parameter passed in create()
    def category(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if extracted:
            for cat in extracted:
                self.category.add(cat)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductType

    name = factory.Sequence(lambda n: "type_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Brand

    name = factory.Sequence(lambda n: "brand_%d" % n)


class ProductInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductInventory

    sku = factory.Sequence(lambda n: "sku_%d" % n)
    upc = factory.Sequence(lambda n: "upc_%d" % n)
    product_type = factory.SubFactory(ProductTypeFactory)
    product = factory.SubFactory(ProductFactory)
    brand = factory.SubFactory(BrandFactory)
    is_active = 1
    retail_price = 97
    store_price = 92
    sale_price = 46
    weight = 987


class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Media

    product_inventory = factory.SubFactory(ProductInventoryFactory)
    image = "images/default.png"
    alt_text = "a default image solid color"
    is_feature = True


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Stock

    product_inventory = factory.SubFactory(ProductInventoryFactory)
    units = 2
    units_sold = 100


class ProductAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductAttribute

    name = factory.Sequence(lambda n: "attribute_name_%d" % n)
    description = factory.Sequence(lambda n: "description_%d" % n)


class ProductAttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductAttributeValue

    product_attribute = factory.SubFactory(ProductAttributeFactory)
    attribute_value = fake.lexify(text="attribute_value_??????")


register(CategoryFactory)
register(ProductFactory)
register(ProductTypeFactory)
register(BrandFactory)
register(ProductInventoryFactory)
register(MediaFactory)
register(StockFactory)
register(ProductAttributeFactory)
register(ProductAttributeValueFactory)
