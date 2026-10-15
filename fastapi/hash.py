import bcrypt


# hashes a raw password string using bcrypt
def generate_password(password: str) -> str:
    pass_to_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pass_to_bytes, salt=salt)
    return hashed_password.decode("utf-8")


# checks whether user's entered password matches the stored bcrypt hash
def check_password(password: str, hashvalue: str) -> bool:
    plain_pass_to_bytes = password.encode("utf-8")
    hash_value_to_bytes = hashvalue.encode("utf-8")
    return bcrypt.checkpw(
        password=plain_pass_to_bytes, hashed_password=hash_value_to_bytes
    )


if __name__ == "__main__":
    # run `python hash.py` directly in terminal to test
    sample_password = "studentpassword123"
    hashed = generate_password(sample_password)
    print("Original:", sample_password)
    print("Hashed:  ", hashed)
    print("Matches? ", check_password(sample_password, hashed))
