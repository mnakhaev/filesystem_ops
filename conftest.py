import random

import pytest

from helpers import generate_random_string


@pytest.fixture
def remove_testdir(tmpdir):
    """Remove testdir after test in finished.
    This fixture is applicable for both testcases with directories and files.

    """
    yield
    if tmpdir.check():
        tmpdir.remove()


@pytest.fixture
def create_testdir(remove_testdir, tmpdir, request):
    """Create tmpdir and remove it after test is finished."""
    dir_name = getattr(request, 'param', generate_random_string())
    tmpdir.mkdir(dir_name)

    yield tmpdir, dir_name


@pytest.fixture
def create_testfile(remove_testdir, tmpdir, request):
    """Create test file with random content and remove the whole testdir after test is finished."""
    filename = getattr(request, 'param', generate_random_string())
    p = tmpdir.join(filename)
    p.write(generate_random_string(random.randint(1, 100)))

    yield tmpdir, filename
