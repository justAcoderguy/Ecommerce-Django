import pytest
from inventory import models

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

