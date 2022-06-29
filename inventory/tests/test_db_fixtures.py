from django.db import IntegrityError
import pytest
from inventory import models

"""
    General naming convention of the pytest marks used in this file:
    - dbfixture : Tests which use a fixture for data
    - dbfactory : Tests which use a factory for data

"""


##################################
####### CATEGORY MODEL ###########
##################################


#### Method 1 - Using Fixtures ####

@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, name, slug, is_active",
    [
        (3, "shoes", "shoes", 1),
        (17, "golf", "golf", 1),
        (33, "halloween", "halloween", 1),
    ]
)
def test_inventory_category_dbfixture(
    db, django_db_fixture_setup, id, name, slug, is_active
):
    """
        Checks if the data added to the database from the category fixture
        is OK using few samples from pytest parametrize.
    """
    category = models.Category.objects.get(id=id)
    assert category.name == name
    assert category.slug == slug
    assert category.is_active == is_active

#### Method 2 - Using Factory(ies) ####


@pytest.mark.dbfactory
@pytest.mark.parametrize(
    "name, slug, is_active",
    [
        ("jumper", "jumper", 1),
        ("shirts", "shirts", 1),
        ("trousers", "trousers", 1),
    ]
)
def test_inventory_db_category_insert_data(
    db, category_factory, name, slug, is_active
):
    """
        Creates Category object using the category factory but using
        default parameters passed from pytest parametrize.
    """
    category = category_factory.create(name=name, slug=slug, is_active=is_active)
    assert category.name == name
    assert category.slug == slug
    assert category.is_active == is_active


@pytest.mark.dbfactory
def test_inventory_db_category_insert_data_using_factory_only(
    db, category_factory
):
    """
        Creates Category object using the category factory but  without
        using default parameters.
    """
    category = category_factory.create()
    category_in_db = models.Category.objects.get(id=category.id)
    assert category.name == category_in_db.name
    assert category.slug == category_in_db.slug
    assert category.is_active == category_in_db.is_active


##################################
####### PRODUCT MODEL ############
##################################

#### Method 1 - Using Fixtures ####

@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, web_id, name, slug, description, is_active, created_at, updated_at",
    [
        (
            1,
            "45425810",
            "widstar running sneakers",
            "widstar-running-sneakers",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.",  # noqa: E501
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
        (
            8616,
            "45434425",
            "impact puse dance shoe",
            "impact-puse-dance-shoe",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.",  # noqa: E501
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
    ]
)
def test_inventory_product_dbfixture(
    db, django_db_fixture_setup, id, web_id, slug, name, description, is_active, created_at, updated_at
):
    """
        Checks if the data added to the database from the product fixture
        is OK using few samples from pytest parametrize.
    """
    product = models.Product.objects.get(id=id)
    product_created_at = product.created_at.strftime("%Y-%m-%d %H:%M:%S")
    product_updated_at = product.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    assert product.web_id == web_id
    assert product.name == name
    assert product.slug == slug
    assert product.description == description
    assert product.is_active == is_active
    assert product_created_at == created_at
    assert product_updated_at == updated_at


#### Method 2 - Using Factory(ies) ####

@pytest.mark.dbfactory
def test_inventory_product_uniqueness_integrity(db, product_factory):
    """
        Test to verify that we can't create two products with the same web id.
        ie. Web-id assigned to a product must be unique
    """
    product = product_factory.create(web_id=12345678)  # noqa
    # https://docs.pytest.org/en/6.2.x/assert.html#assertions-about-expected-exceptions
    with pytest.raises(IntegrityError):
        product_factory.create(web_id=12345678)


@pytest.mark.dbfixture
@pytest.mark.dbfactory
def test_inventory_db_product_insert_data(db, product_factory, django_db_fixture_setup):
    """
        This uses both fixture and factory mark because this test is using category data
        from category fixture and a product object is created from product factory.

        'django_db_fixture_setup' is added here in the parameters just for understanding ,
        but it is not needed because the fixture is scoped as 'session' and running any
        previous dbfixture marked test would be sufficient as the data would be stored in db
        for current testing session.

        NOTE: if only dbfactory mark tests were run, then the django_db_fixture_Setup
        would be required since no other fixture tests are being run to create the session wide
        database data.

        This test tests the creation of a new product object using the product factory.
    """
    # We are passing the categories here which then uses post_generation decorator
    # in the product factory
    new_product = product_factory.create(category=(1, 2, 3, 4, 5))
    result_product_category_number = new_product.category.all().count()
    assert result_product_category_number == 5


##################################
#### PRODUCT INVENTORY MODEL #####
##################################

######## Using Fixtures ##########

"""
    Product Inventory is used to distinguish between the variants of a product.
    Eg. A XYZ brand of shoe may have 3 colours. All 3 are different fields in the
    product inventory table but they are essentially the same XYZ brand of shoe in
    the product table.
"""


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, sku, upc, product_type, product, brand, is_active, retail_price, store_price, sale_price,\
    weight, created_at, updated_at",
    [
        (
            1,
            "7633969397",
            "100000000001",
            1,
            1,
            1,
            1,
            97.00,
            92.00,
            46.00,
            987,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
        (
            8616,
            "3880741573",
            "100000008616",
            1,
            8616,
            1253,
            1,
            89.00,
            84.00,
            42.00,
            929,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
    ],
)
def test_inventory_db_product_inventory_dbfixture(

    db,
    django_db_fixture_setup,
    id,
    sku,
    upc,
    product_type,
    product,
    brand,
    is_active,
    retail_price,
    store_price,
    sale_price,
    weight,
    created_at,
    updated_at,
):
    """
        Checks if the data added to the database from the product inventory
        fixture is OK using few samples from pytest parametrize.
    """
    result = models.ProductInventory.objects.get(id=id)
    result_created_at = result.created_at.strftime("%Y-%m-%d %H:%M:%S")
    result_updated_at = result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    assert result.sku == sku
    assert result.upc == upc
    assert result.product_type.id == product_type
    assert result.product.id == product
    assert result.brand.id == brand
    assert result.is_active == is_active
    assert result.retail_price == retail_price
    assert result.store_price == store_price
    assert result.sale_price == sale_price
    assert result.weight == weight
    assert result_created_at == created_at
    assert result_updated_at == updated_at


def test_inventory_product_inventory_insert_data(
    db, product_inventory_factory
):
    """
        This test tests the creation of a new product inventory object using the product
        inventory factory.
    """
    new_product_inventory = product_inventory_factory.create(
        sku="123456789",
        upc="123456789",
        product_type__name="new_name",
        product__web_id="123456789",
        brand__name="new_name",
    )
    assert new_product_inventory.sku == "123456789"
    assert new_product_inventory.upc == "123456789"
    assert new_product_inventory.product_type.name == "new_name"
    assert new_product_inventory.product.web_id == "123456789"
    assert new_product_inventory.brand.name == "new_name"
    assert new_product_inventory.is_active == 1
    assert new_product_inventory.retail_price == 97.00
    assert new_product_inventory.store_price == 92.00
    assert new_product_inventory.sale_price == 46.00
    assert new_product_inventory.weight == 987

##################################
###### PRODUCT TYPE MODEL ########
##################################

# Method 2 - Using Factory


@pytest.mark.dbfactory
def test_inventory_product_type_insert_data(
    db, product_type_factory
):
    new_prod_type = product_type_factory.create(name="new_type")
    assert new_prod_type.name == "new_type"


@pytest.mark.dbfactory
def test_inventory_product_type_uniqueness_integrity(db, product_type_factory):
    new_prod_type = product_type_factory.create(name="new_type")  # noqa

    # https://docs.pytest.org/en/6.2.x/assert.html#assertions-about-expected-exceptions
    with pytest.raises(IntegrityError):
        product_type_factory.create(name="new_type")


##################################
######### BRAND MODEL ############
##################################

# # Method 2 - Using Factory


@pytest.mark.dbfactory
def test_inventory_brand_insert_data(
    db, brand_factory
):
    new_brand = brand_factory.create(name="new_brand")
    assert new_brand.name == "new_brand"


@pytest.mark.dbfactory
def test_inventory_brand_uniqueness_integrity(db, brand_factory):
    new_brand = brand_factory.create(name="new_brand")  # noqa

    # https://docs.pytest.org/en/6.2.x/assert.html#assertions-about-expected-exceptions
    with pytest.raises(IntegrityError):
        brand_factory.create(name="new_brand")


##################################
######## MEDIA MODEL #############
##################################

@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, product_inventory, image, alt_text, is_feature, created_at, updated_at",
    [
        (
            1,
            1,
            "images/default.png",
            "a default image solid color",
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
        (
            8616,
            8616,
            "images/default.png",
            "a default image solid color",
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
    ],
)
def test_inventory_db_media_fixture(
    db,
    django_db_fixture_setup,
    id,
    product_inventory,
    image,
    alt_text,
    is_feature,
    created_at,
    updated_at,
):
    result = models.Media.objects.get(id=id)
    result_created_at = result.created_at.strftime("%Y-%m-%d %H:%M:%S")
    result_updated_at = result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    assert result.product_inventory.id == product_inventory
    assert result.image == image
    assert result.alt_text == alt_text
    assert result.is_feature == is_feature
    assert result_created_at == created_at
    assert result_updated_at == updated_at


def test_inventory_db_media_insert_data(db, media_factory):
    new_media = media_factory.create(product_inventory__sku="123456789")
    assert new_media.product_inventory.sku == "123456789"
    assert new_media.image == "images/default.png"
    assert new_media.alt_text == "a default image solid color"
    assert new_media.is_feature == 1


##################################
######## STOCK MODEL #############
##################################

@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, product_inventory, last_checked, units, units_sold",
    [
        (1, 1, "2021-09-04 22:14:18", 135, 0),
        (8616, 8616, "2021-09-04 22:14:18", 100, 0),
    ],
)
def test_inventory_db_stock_dataset(
    db,
    django_db_fixture_setup,
    id,
    product_inventory,
    last_checked,
    units,
    units_sold,
):
    result = models.Stock.objects.get(id=id)
    result_last_checked = result.last_checked.strftime("%Y-%m-%d %H:%M:%S")
    assert result.product_inventory.id == product_inventory
    assert result_last_checked == last_checked
    assert result.units == units
    assert result.units_sold == units_sold


def test_inventory_db_stock_insert_data(db, stock_factory):
    new_stock = stock_factory.create(product_inventory__sku="123456789")
    assert new_stock.product_inventory.sku == "123456789"
    assert new_stock.units == 2
    assert new_stock.units_sold == 100
    assert new_stock.units_sold == 100
    assert new_stock.units_sold == 100

#test if CI is active .