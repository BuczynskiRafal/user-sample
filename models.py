"""Module containing method for create user objects and manage data in database."""
import sqlite3

from password_validators.validators import PasswordValidator
from email_validator import validate_email, EmailNotValidError


class CreateUserDb:
    """Database commands."""


def connect_with_db(func):
    """Create connection with DB."""
    def wrapper():
        conn = sqlite3.connect("user.sqlite3")
        cur = conn.cursor()
        func_work = func(cur=cur)
        conn.commit()
        conn.close()
        return func_work

    return wrapper


@connect_with_db
def create_db(cur):
    """Create user table in DB."""
    query = """DROP TABLE IF EXISTS "user";
            CREATE TABLE IF NOT EXISTS "user" (
            "id" integer NOT NULL
            , "username" text NOT NULL
            , "password" text NOT NULL
            , "email" text NOT NULL
            , PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    cur.executescript(query)
    return "Created"


@connect_with_db
def check_if_exist(cur):
    """Check if user table exist in DB."""
    query = """
    SELECT count(*) FROM "user";
    """
    cur.execute(query)
    return len(cur.fetchall()[0]) > 0


@connect_with_db
def show_table(cur):
    """Print all rows form user table."""
    query = """
    SELECT * FROM "user";
    """
    cur.execute(query)
    return cur.fetchall()[0]


@connect_with_db
def add_user_to_db(cur):
    """Create user in user table"""
    if check_if_exist() is False:
        create_db()
    record = """BEGIN TRANSACTION;
    INSERT INTO "user" ("id","username","password","email") VALUES (1,'first user','test_password','test_email');
    COMMIT;
    """
    cur.executescript(record)
    return show_table()

class User:
    """Create valid user class"""

    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f"Class: {__class__.__name__}, " \
               f"username: {self.username}, password: {self.password}, email: {self.email}"

    def __str__(self):
        return f"User: {self.username}"

    @property
    def password(self):
        """Get the current password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set the current password."""
        user_obj = PasswordValidator(value)
        if not user_obj.is_validate():
            raise user_obj.errors[0]
        self._password = value

    @password.getter
    def password(self):
        """Get the current password."""
        return self._password

    @property
    def email(self):
        """Get the current email."""
        return self._email

    @email.setter
    def email(self, value):
        """Set the current email."""
        try:
            if validate_email(value):
                self._email = value
        except EmailNotValidError as error:
            raise error

    @email.getter
    def email(self):
        """Get the current email."""
        return self._email