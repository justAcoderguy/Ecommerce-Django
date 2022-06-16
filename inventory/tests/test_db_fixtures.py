import pytest
from inventory import models

#### Method 1 - Using Fixtures ####

@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id, name, slug, is_active",
    [
        (1, "shoes", "shoes", 1),
        (14, "shirts", "shirts", 1),
        (30, "trousers", "trousers", 1),
    ]
)
def test_inventory_category_dbfixture(
    db, django_db_fixture_setup, id, name, slug, is_active
):
    category = models.Category.objects.get(id=id)
    assert category.name == name
    assert category.slug == slug
    assert category.is_active == is_active 

#### Method 2 - Using Factory(ies) ####

@pytest.mark.parametrize(
    "name, slug, is_active",
    [
        ("shoes", "shoes", 1),
        ("shirts", "shirts", 1),
        ("trousers", "trousers", 1),
    ]
)
def test_inventory_db_category_insert_data(
    db, category_factory, name, slug, is_active
):
    category = category_factory.create(name=name, slug=slug, is_active=is_active)
    assert category.name == name
    assert category.slug == slug
    assert category.is_active == is_active 