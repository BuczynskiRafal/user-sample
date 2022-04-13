import pytest

from models import User
from password_validators.exceptions.exceptions import ValidationError
from password_validators.validators import PasswordValidator
from email_validator import EmailSyntaxError, EmailNotValidError, EmailUndeliverableError, ValidatedEmail


class TestUserPassword:
    def test_set_password_no_numbers(self, t_user_valid):
        with pytest.raises(ValidationError) as error:
            expected = 'Password must contain one or more upper letter.'
            t_user_valid.password = 'Ascqsdc.!'
            assert expected == error.value

    def test_set_password_invalid_length(self, t_user_valid):
        with pytest.raises(ValidationError) as error:
            expected = 'Password is too short.'
            t_user_valid.password = 'Qsdc1.!'
            assert expected == error.value

    def test_set_password_invalid_special_character(self, t_user_valid):
        with pytest.raises(ValidationError) as error:
            expected = 'Password must contain at least one special characters.'
            t_user_valid.password = 'Qsdc1ass'
            assert expected == error.value

    def test_set_password_invalid_upper_character(self, t_user_valid):
        with pytest.raises(ValidationError) as error:
            expected = 'Password must contain one or more upper letter.'
            t_user_valid.password = 'qsdc1ass!'
            assert expected == error.value

    def test_set_password_invalid_lower_character(self, t_user_valid):
        with pytest.raises(ValidationError) as error:
            expected = 'Password must contain or more lower letter.'
            t_user_valid.password = 'QQSQWDWDWWDWD1!.'
            assert expected == error.value

    def test_set_password_leaked_password(self, t_user_valid):
        with pytest.raises(ValidationError) as error:
            expected = 'Password must contain or more lower letter.'
            t_user_valid.password = 'Qwerty123!'
            assert expected == error.value

    def test_set_password_no_errors(self, t_user_valid):
        t_user_valid.password = 'Qsdcrsdc1234.!'
        assert t_user_valid.password == 'Qsdcrsdc1234.!'


class TestUserEmail:
    def test_set_email_no_a_sign(self, t_user_valid):
        with pytest.raises(ValueError) as error:
            expected = 'The email address is not valid. It must have exactly one @-sign.'
            t_user_valid.email = 'mailmail.c'
            assert expected == error.value

    def test_set_email_domain_does_not_exist(self, t_user_valid):
        with pytest.raises(EmailUndeliverableError) as error:
            expected = 'The domain name mail.c does not exist.'
            t_user_valid.email = 'mail@mail.c'
            assert expected == error.value

            expected = 'The domain name m.com does not exist.'
            t_user_valid.email = 'mail@m.com'
            assert expected == error.value

    def test_set_email_dot_after_a_sign(self, t_user_valid):
        with pytest.raises(EmailSyntaxError) as error:
            expected = 'An email address cannot have a period immediately after the @-sign.'
            t_user_valid.email = 'mail@.com'
            assert expected == error.value

    def test_set_email_end_with_dot(self, t_user_valid):
        with pytest.raises(EmailSyntaxError) as error:
            expected = 'An email address cannot end with a period.'
            t_user_valid.email = 'mail@.'
            assert expected == error.value

    def test_set_email_start_with_dot(self, t_user_valid):
        with pytest.raises(EmailSyntaxError) as error:
            expected = 'There must be something before the @-sign.'
            t_user_valid.email = '@mail.com'
            assert expected == error.value


