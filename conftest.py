from pytest import fixture

from models import User


@fixture
def t_user_valid():
    return User('test_user', 'Qsdcrsdc123.!', 'mail@mail.com')
