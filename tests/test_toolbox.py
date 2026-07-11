import unittest
import os
import tempfile
import sys
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), '../pc_toolbox'))

from i18n import I18N
from vault import SecureVault

class TestCyberToolbox(unittest.TestCase):

    def test_translation_switch(self):
        """Verify dynamic locale language translation switching operates properly."""
        i18n = I18N("en")
        self.assertEqual(i18n.get("app_title"), "NEO-GEN SENSORY CYBER COMMAND")

        # Switch language to Turkish
        i18n.set_language("tr")
        self.assertEqual(i18n.get("app_title"), "NEO-GEN SİBER KOMUTA MERKEZİ")

        # Switch language to Spanish
        i18n.set_language("es")
        self.assertEqual(i18n.get("app_title"), "NEO-GEN COMANDO CIBERNÉTICO HUD")

    def test_secure_messaging_crypto(self):
        """Verify AES-256 secure messaging encryption and decryption works flawlessly."""
        passphrase = "master_cyber_key_1337"
        plaintext = "This is a highly confidential hack mission message!"

        # Encrypt
        ciphertext = SecureVault.encrypt_message(plaintext, passphrase)
        self.assertNotEqual(plaintext, ciphertext)
        self.assertTrue(len(ciphertext) > 0)

        # Decrypt
        decrypted = SecureVault.decrypt_message(ciphertext, passphrase)
        self.assertEqual(plaintext, decrypted)

    def test_secure_messaging_empty_key(self):
        """Verify cryptography handling rejects empty encryption keys."""
        with self.assertRaises(ValueError):
            SecureVault.encrypt_message("secret", "")

    def test_hash_generation(self):
        """Verify correct file hashing using SHA-256 and MD5."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_file = os.path.join(tmpdir, "hash_test.txt")
            with open(temp_file, "w") as f:
                f.write("Cyber Matrix Code")

            sha256_val = SecureVault.generate_file_hash(temp_file, "sha256")
            md5_val = SecureVault.generate_file_hash(temp_file, "md5")

            self.assertTrue(len(sha256_val) == 64)
            self.assertTrue(len(md5_val) == 32)

    def test_exif_removal_utility(self):
        """Verify metadata exif remover produces a clean scrubbed image."""
        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = os.path.join(tmpdir, "test_img.png")
            out_path = os.path.join(tmpdir, "test_img_clean.png")

            # Create dummy image
            img = Image.new('RGB', (100, 100), color='green')
            img.save(img_path)

            status = SecureVault.remove_exif_metadata(img_path, out_path)
            self.assertTrue(status)
            self.assertTrue(os.path.exists(out_path))

    def test_steganography_hide_extract(self):
        """Verify text is correctly hidden and extracted using LSB Steganography."""
        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = os.path.join(tmpdir, "steg_carrier.png")
            out_path = os.path.join(tmpdir, "steg_out.png")

            # Create a larger base image to accommodate secret message bit requirements
            img = Image.new('RGBA', (200, 200), color='black')
            img.save(img_path)

            secret_msg = "Follow the White Rabbit."
            status = SecureVault.hide_secret_text_steg(img_path, secret_msg, out_path)
            self.assertTrue(status)
            self.assertTrue(os.path.exists(out_path))

            extracted = SecureVault.extract_secret_text_steg(out_path)
            self.assertEqual(secret_msg, extracted)

if __name__ == "__main__":
    unittest.main()
