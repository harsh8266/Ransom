import base64
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Set the decryption key for AES
decryption_key = b"my_decryption_key"

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

# Decrypt all the .encrypted files in the current directory and subdirectories
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".encrypted"):
            encrypted_file_path = os.path.join(root, file)
            with open(encrypted_file_path, "r") as encrypted_file:
                # Read the IV and encrypted contents from the file
                iv = encrypted_file.readline().strip()
                encrypted_contents = encrypted_file.read()

                # Decrypt the file
                decrypted_contents = decrypt_file(iv, encrypted_contents, decryption_key)

            # Write the decrypted contents to a new file
            decrypted_file_path = encrypted_file_path[:-10]
            with open(decrypted_file_path, "wb") as decrypted_file:
                decrypted_file.write(decrypted_contents)

            # Delete the encrypted file
            os.remove(encrypted_file_path)

print("Files decrypted successfully!")
