from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hmac
import os

def generate_rsa_key_pair(key_size=2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_private_key_to_file(private_key, filename):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as key_file:
        key_file.write(pem)

def load_private_key_from_file(filename):
    with open(filename, 'rb') as key_file:
        private_key_data = key_file.read()
        private_key = serialization.load_pem_private_key(private_key_data, password=None, backend=default_backend())
    return private_key

def encrypt_image_with_rsa(image_filename, public_key, output_filename):
    with open(image_filename, 'rb') as image_file:
        image_data = image_file.read()

    ciphertext = public_key.encrypt(
        image_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_filename, 'wb') as encrypted_image_file:
        encrypted_image_file.write(ciphertext)

def decrypt_image_with_rsa(encrypted_image_filename, private_key, output_filename):
    with open(encrypted_image_filename, 'rb') as encrypted_image_file:
        ciphertext = encrypted_image_file.read()

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(output_filename, 'wb') as decrypted_image_file:
        decrypted_image_file.write(plaintext)

if __name__ == "__main__":
    # Generate RSA key pair
    private_key, public_key = generate_rsa_key_pair()

    # Save private key to a file (keep this private)
    save_private_key_to_file(private_key, "private_key.pem")

    # Encrypt an image
    image_filename = "input_image.jpg"
    encrypted_image_filename = "encrypted_image.bin"
    encrypt_image_with_rsa(image_filename, public_key, encrypted_image_filename)
    print("Image encrypted.")

    # Decrypt the encrypted image
    private_key = load_private_key_from_file("private_key.pem")
    decrypted_image_filename = "decrypted_image.jpg"
    decrypt_image_with_rsa(encrypted_image_filename, private_key, decrypted_image_filename)
    print("Image decrypted.")
