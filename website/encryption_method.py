import random

class CaesarEncryption:
    def __init__(self, text: str, used_codes: list[int]):
        self.generated_shift = self.generate_shift()
        self.encrypted_text = self.caesar_encrypt(string=text, shift=self.generated_shift)
        self.code = self.generate_code(used_codes)


    def generate_code(self, used_codes: list[int]):
        while True:
            random_code = [str(random.randint(1, 9)) for _ in range(6)]
            random_code = int("".join(random_code))
            if (random_code not in used_codes) and len(str(random_code)) == 6:
                break
        return random_code

    def generate_shift(self):
        return random.randint(1, 9)

    def caesar_encrypt(self, string: str, shift: int):
        string_to_encrypt = string.lower()

        ciphertext = ""
        for char in string_to_encrypt:
            shifted = (ord(char) + shift) % 256
            ciphertext += chr(shifted)

        return ciphertext


class CaesarDecryption:
    def __init__(self, text: str, shift: int):
        self.decrypted_text = self.caesar_decrypt(text, shift)


    def caesar_decrypt(self, string: str, shift: int):
        string_to_decrypt = string.lower()

        plaintext = ""
        for char in string_to_decrypt:
            shifted = (ord(char) - shift) % 256
            plaintext += chr(shifted)

        return plaintext


