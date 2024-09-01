from app.auth.hash import generate_password_hash, verify_password


def test_generate_hash():
    password = '123456'
    hashed = generate_password_hash(password)

    assert verify_password(password, hashed)
