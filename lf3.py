import os
import tarfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import argparse

class LF3Decryptor:
    def __init__(self):
        self.file_in = ""
        self.cache_folder = r"[CHANGE ME]"
        self.decrypted_folder = r"[CHANGE ME]"
        self.has_decrypted = False

        if self.cache_folder == "[CHANGE ME]" or self.decrypted_folder == "[CHANGE ME]":
            print("You need to change folder locations within the script.")
            exit()

        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)

    def init_ctr(self, key, iv):
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        return cipher

    def decrypt_ctr(self, cipher, data):
        decryptor = cipher.decryptor()
        return decryptor.update(data) + decryptor.finalize()

    def lf3_decrypt(self, file_input):
        self.file_in = file_input
        print(f"Decrypting {self.file_in}...")

        key = b'\x44\xee\x33\x41\x4a\x56\x48\xe1\x5e\x1c\x7e\x15\x85\xb1\x07\x38'
        iv = bytearray(16)

        cipher = self.init_ctr(key, iv)

        try:
            with open(self.file_in, 'rb') as file_stream1:
                file_stream1.seek(0)
                num_array1 = file_stream1.read(16)
                cipher = self.init_ctr(key, num_array1)
                num_array2 = file_stream1.read()
                
                buffer = self.decrypt_ctr(cipher, num_array2)

                decrypted_tar_path = os.path.join(self.cache_folder, os.path.splitext(os.path.basename(self.file_in))[0] + ".tar")
                
                with open(decrypted_tar_path, 'wb') as file_stream2:
                    file_stream2.write(buffer)

                if os.path.exists(decrypted_tar_path):
                    extracted_folder = os.path.splitext(os.path.basename(self.file_in))[0]
                    destination_path = os.path.join(self.decrypted_folder, extracted_folder)
                    self.extract_tar(decrypted_tar_path, destination_path)
                    os.remove(decrypted_tar_path)
                    print(f"Extraction completed. Files placed in '{destination_path}'.")
                    self.has_decrypted = True  # Set decryption success flag

                    if os.path.exists(os.path.join(self.cache_folder, os.path.basename(self.file_in))):
                        if not os.path.exists(self.decrypted_folder):
                            os.makedirs(self.decrypted_folder)
                        if self.move_decrypted_files(os.path.basename(self.file_in), extracted_folder):
                            print("Decryption completed.")
                        os.remove(os.path.join(self.cache_folder, os.path.basename(self.file_in)))

        except FileNotFoundError:
            print(f"File not found: {self.file_in}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Decryption Failed")

    def extract_tar(self, tar_file, destination_path):
        try:
            with tarfile.open(tar_file, 'r') as tar:
                tar.extractall(destination_path)
        except Exception as e:
            print(f"An error occurred during extraction: {e}")

    def move_decrypted_files(self, file_in, extracted_folder):
        source_folder = os.path.join(self.decrypted_folder, extracted_folder)
        try:
            if os.path.exists(source_folder):
                return True
            return False
        except Exception as e:
            print(f"An error occurred while moving decrypted files: {e}")
            return False

    def decrypt_folder(self, folder_path):
        lf3_files = [f for f in os.listdir(folder_path) if f.endswith(".lf3")]

        if not lf3_files:
            print(f"No .lf3 files found in the folder: {folder_path}")
            return

        for lf3_file in lf3_files:
            lf3_file_path = os.path.join(folder_path, lf3_file)
            self.lf3_decrypt(lf3_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LF3 Decryptor Script")
    parser.add_argument("input_path", help="Path to the file or folder to decrypt")

    args = parser.parse_args()

    lf3_decryptor = LF3Decryptor()

    if os.path.isfile(args.input_path):
        lf3_decryptor.lf3_decrypt(args.input_path)
    elif os.path.isdir(args.input_path):
        lf3_decryptor.decrypt_folder(args.input_path)
    else:
        print("Invalid input path. Please provide a valid file or folder path.")
