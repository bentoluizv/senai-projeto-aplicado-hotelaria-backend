from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def generate_password_hash(pwd: str):
    return pwd_context.hash(pwd)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
