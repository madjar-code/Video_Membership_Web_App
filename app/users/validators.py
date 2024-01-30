from email_validator import (
    EmailNotValidError,
    validate_email,
)


def _validate_email(email):
    message = ''
    valid = False
    try:
        valid = validate_email(email)
        # update the email var with a normalized value
        email = valid.email
        valid = True
    except EmailNotValidError as e:
        message = str(e)
    return valid, message, email
