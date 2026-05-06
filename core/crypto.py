import os
import base64
from hashlib import pbkdf2_hmac
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
ITERATIONS = 100_000


# ===== КЛЮЧ ИЗ ПАРОЛЯ =====
def generate_key(password: str, salt: bytes):
    key = pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        ITERATIONS
    )
    return base64.urlsafe_b64encode(key)


# ===== ШИФРОВАНИЕ С УДАЛЕНИЕМ ОРИГИНАЛА =====
def encrypt_file(filepath, password):
    salt = os.urandom(16)
    key = generate_key(password, salt)
    cipher = Fernet(key)

    with open(filepath, 'rb') as f:
        data = f.read()

    encrypted = cipher.encrypt(data)

    enc_path = filepath + ".enc"

    with open(enc_path, 'wb') as f:
        f.write(salt + encrypted)

    # 🔥 УДАЛЕНИЕ ОРИГИНАЛЬНОГО ФАЙЛА
    try:
        os.remove(filepath)
    except Exception as e:
        print("Не удалось удалить файл:", e)

    return enc_path


# ===== РАСШИФРОВКА ФАЙЛА =====
def decrypt_file(filepath, password):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        salt = data[:16]
        encrypted = data[16:]

        key = generate_key(password, salt)
        cipher = Fernet(key)

        decrypted = cipher.decrypt(encrypted)

        output = filepath.replace('.enc', '')

        with open(output, 'wb') as f:
            f.write(decrypted)

    except InvalidToken:
        raise Exception("Неверный пароль или повреждённый файл")

# ===== ПАПКА (пока просто сбор файлов) =====
def get_all_files(folder):
    files = []

    for root, _, filenames in os.walk(folder):
        for f in filenames:
            files.append(os.path.join(root, f))

    return files
