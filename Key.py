import hashlib

# Set the password
password = "my_password"

# Set the salt
salt = b"my_salt"

# Set the number of iterations for the PBKDF function
iterations = 100000

# Generate the AES key
key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)

print(key)
