import pytest
from django.core.management import call_command

@pytest.fixture
def create_superuser(django_user_model):
    """
    Returs an admin user
    """
    return django_user_model.objects.create_superuser("admin", "a@a", "password")

@pytest.fixture(scope="session")
def django_db_fixture_setup(django_db_setup, django_db_blocker):
    """
    Load a test DB with data from fixture
    """
    with django_db_blocker.unblock(): 
        call_command("loaddata", "db_admin_fixture.json")
        call_command("loaddata", "db_category_fixture.json")
