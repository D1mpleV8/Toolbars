import os
import base64
import hashlib
import zipfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from PIL import Image

class SecureVault:
    """
    Implements AES-256 secure messaging, ZIP-based secure archiving,
    universal format converter fallbacks, and Cyber-ops utility functions (Hashes, EXIF, Steg).
    """

    @staticmethod
    def _derive_key(passphrase: str, salt: bytes) -> bytes:
        """Derive a cryptographically strong 256-bit key from passphrase using PBKDF2 with SHA256."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(passphrase.encode('utf-8'))

    @classmethod
    def encrypt_message(cls, plaintext: str, passphrase: str) -> str:
        """AES-256-CBC Encrypts text securely with a passphrase."""
        if not passphrase:
            raise ValueError("Passphrase cannot be empty.")
        salt = os.urandom(16)
        key = cls._derive_key(passphrase, salt)
        iv = os.urandom(16)

        # Padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Combine Salt + IV + Ciphertext
        combined = salt + iv + ciphertext
        return base64.b64encode(combined).decode('utf-8')

    @classmethod
    def decrypt_message(cls, encrypted_b64: str, passphrase: str) -> str:
        """AES-256-CBC Decrypts text securely with a passphrase."""
        if not passphrase:
            raise ValueError("Passphrase cannot be empty.")
        try:
            combined = base64.b64decode(encrypted_b64.encode('utf-8'))
            if len(combined) < 32:
                raise ValueError("Invalid encrypted message structure.")

            salt = combined[:16]
            iv = combined[16:32]
            ciphertext = combined[32:]

            key = cls._derive_key(passphrase, salt)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            return data.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    @staticmethod
    def create_secure_archive(source_filepaths, output_archive_path, callback=None):
        """
        Creates a high-speed, multi-format ZIP archive (futuristic progress updates).
        """
        total = len(source_filepaths)
        with zipfile.ZipFile(output_archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for idx, filepath in enumerate(source_filepaths):
                if os.path.exists(filepath):
                    zipf.write(filepath, os.path.basename(filepath))
                if callback:
                    callback(int(((idx + 1) / total) * 100))
        return True

    @staticmethod
    def extract_secure_archive(archive_path, output_dir, callback=None):
        """
        Extracts ZIP files locally (futuristic progress updates).
        """
        if not os.path.exists(archive_path):
            return False
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            namelist = zipf.namelist()
            total = len(namelist)
            os.makedirs(output_dir, exist_ok=True)
            for idx, member in enumerate(namelist):
                zipf.extract(member, output_dir)
                if callback:
                    callback(int(((idx + 1) / total) * 100))
        return True

    @staticmethod
    def local_format_convert(input_path, output_path):
        """
        Converts media and image file formats locally using PIL (Pillow) or system libraries.
        Supports offline image conversions (PNG -> JPG, JPG -> PNG, WEBP, etc.)
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError("Source file not found.")

        # Standard Offline Image Converter
        img = Image.open(input_path)
        img.save(output_path)
        return True

    @staticmethod
    def generate_file_hash(filepath, algorithm="sha256"):
        """
        Generates SHA-256 or MD5 hash check sum of a file.
        """
        if not os.path.exists(filepath):
            return ""
        hasher = hashlib.sha256() if algorithm == "sha256" else hashlib.md5()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def remove_exif_metadata(image_path, output_path):
        """
        Removes EXIF metadata for privacy reasons.
        """
        if not os.path.exists(image_path):
            return False
        image = Image.open(image_path)
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(output_path)
        return True

    @staticmethod
    def hide_secret_text_steg(image_path, secret_text, output_path):
        """
        Least Significant Bit (LSB) Steganography to hide text inside images.
        """
        if not os.path.exists(image_path):
            return False
        image = Image.open(image_path).convert('RGBA')

        # Prepare secret data binary string (ends with standard cyber sentinel)
        sentinel = "##CYBER##"
        binary_secret = ''.join(format(ord(char), '08b') for char in (secret_text + sentinel))

        pixels = image.load()
        width, height = image.size

        bin_idx = 0
        for y in range(height):
            for x in range(width):
                if bin_idx >= len(binary_secret):
                    break
                r, g, b, a = pixels[x, y]

                # Replace LSB of Red channel with secret bit
                bit = int(binary_secret[bin_idx])
                r = (r & 0xFE) | bit
                bin_idx += 1

                pixels[x, y] = (r, g, b, a)
            if bin_idx >= len(binary_secret):
                break

        image.save(output_path)
        return True

    @staticmethod
    def extract_secret_text_steg(image_path):
        """
        Extracts LSB hidden text from stego images.
        """
        if not os.path.exists(image_path):
            return ""
        image = Image.open(image_path).convert('RGBA')
        width, height = image.size

        binary_data = []
        pixels = image.load()
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                binary_data.append(str(r & 1))

        # Convert binary string chunks of 8-bits to chars
        binary_str = "".join(binary_data)
        extracted_text = ""
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i+8]
            if len(byte) < 8:
                break
            char = chr(int(byte, 2))
            extracted_text += char

            # Stop if our sentinel signature is matched
            if "##CYBER##" in extracted_text:
                return extracted_text.split("##CYBER##")[0]
        return ""
