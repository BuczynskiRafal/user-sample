"""Run this file to create user or test safe-password module."""
from models import User, connect_with_db, create_db, check_if_exist, show_table, add_user_to_db

if __name__ == '__main__':
    """Create test user"""
    user_object = User('test user', 'qw1sdklcsdc..F', 'mail@mail.com')
    print(user_object)
