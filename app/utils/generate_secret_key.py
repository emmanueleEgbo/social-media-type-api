import secrets

# GENERATE a 256-bit (32-bytes) hex token

secret_key = secrets.token_hex(32)
print(secret_key)