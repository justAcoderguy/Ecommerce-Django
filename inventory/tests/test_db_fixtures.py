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
    category_in_db = models.Category.objects.get(id = category.id)
    print(category.name)
    assert category.name == category_in_db.name
    assert category.slug == category_in_db.slug
    assert category.is_active == category_in_db.is_active


##################################
####### PRODUCT MODEL ###########
##################################

#### Method 1 - Using Fixtures ####

@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, web_id, slug, name, description, is_active, created_at, updated_at",
    [
        (
            1,
            "45425810",
            "widstar running sneakers",
            "widstar-running-sneakers",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.",
            1,
            "2021-09-04 22:14:18",
            "2021-09-04 22:14:18",
        ),
        (
            8616,
            "45434425",
            "impact puse dance shoe",
            "impact-puse-dance-shoe",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.",
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
    product = product_factory.create(web_id=12345678)
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

        This test tests the creation of a new product object using the product factory.  
    """

    new_product = product_factory.create(category=(1, 2, 3, 4, 5))
    result_product_category = new_product.category.all().count()
    assert "web_id_" in new_product.web_id
    assert result_product_category == 5
