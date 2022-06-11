import pytest

@pytest.fixture
def create_superuser(django_user_model):
    """
    Returs an admin user
    """
    return django_user_model.objects.create_superuser("admin", "a@a", "password")
