from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def generate_hash(pw_raw):
    pw_hash = PasswordHasher()
    return pw_hash.hash(pw_raw)


def verify_hash(pw_hash, pw_raw):
    ph = PasswordHasher()
    verified = False
    msg = ""
    try:
        verified = ph.verify(pw_hash, pw_raw)
    except VerifyMismatchError:
        verified = False
        msg = 'Invalid password'
    except Exception as e:
        verified = False
        msg = f'Unexcepted error:\n {e}'
    return verified, msg
