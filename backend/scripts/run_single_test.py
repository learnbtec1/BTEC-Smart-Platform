import pytest
import sys

if __name__ == '__main__':
    sys.exit(pytest.main(["-q","tests/api/routes/test_users.py::test_get_users_superuser_me"]))
