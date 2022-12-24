import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Set the password
password = "thisi"
# Set the salt
salt = b"1234"
# Set the number of iterations for the PBKDF function
iterations = 100000

# Generate the AES key
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=iterations
)
key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

print(key)
