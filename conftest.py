## ROOT/GLOBAL CONFTEST FILE ##

# File that runs different modules or such , before running any texts
# This file is inspected before running any tests
# For fixtures or factories being set up

# Ran before all tests are started in entire project.
pytest_plugins = [
    "main.tests.fixtures",
    "main.tests.selenium",
    "main.tests.factory",
]
