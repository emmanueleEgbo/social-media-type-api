from pwdlib import PasswordHash

hash_password = PasswordHash.recommended()

# PASSWORD HASHING
def hash_func(user_password: str) -> str:
    return hash_password.hash(user_password)

# PASSWORD VERIFICATION 
def verify_password_func(user_password: str, hashed_password: str) -> bool:
    return hash_password.verify(user_password, hashed_password)