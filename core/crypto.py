import os
import base64
import shutil
from hashlib import pbkdf2_hmac
from cryptography.fernet import Fernet, InvalidToken

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


# ===== ШИФРОВАНИЕ ФАЙЛА (С УДАЛЕНИЕМ ОРИГИНАЛА) =====
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

    # Удаление оригинального файла после шифрования
    try:
        os.remove(filepath)
    except Exception as e:
        print(f"Не удалось удалить оригинальный файл {filepath}: {e}")

    return enc_path


# ===== РАСШИФРОВКА ФАЙЛА (С УДАЛЕНИЕМ ИСХОДНОГО .enc) =====
def decrypt_file(filepath, password):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        salt = data[:16]
        encrypted = data[16:]

        key = generate_key(password, salt)
        cipher = Fernet(key)

        decrypted = cipher.decrypt(encrypted)

        # Убираем расширение .enc
        output = filepath.replace('.enc', '')

        with open(output, 'wb') as f:
            f.write(decrypted)

        # 🔥 ИСПРАВЛЕНИЕ: Удаляем зашифрованный (.enc) файл после успешного восстановления оригинала
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Не удалось удалить зашифрованный файл {filepath}: {e}")

    except InvalidToken:
        raise Exception("Неверный пароль или повреждённый файл")


# ===== ШИФРОВАНИЕ ПАПКИ (АРХИВАЦИЯ + ШИФРОВАНИЕ) =====
def encrypt_folder(folderpath, password):
    if not os.path.exists(folderpath):
        raise Exception("Папка не найдена")

    # Создаем временный zip-архив из папки
    archive_path = shutil.make_archive(folderpath, 'zip', folderpath)
    
    # Шифруем получившийся zip-архив. Появится файл папка.zip.enc
    encrypt_file(archive_path, password)

    # 🔥 Удаляем исходную папку со всем содержимым
    try:
        shutil.rmtree(folderpath)
    except Exception as e:
        print(f"Не удалось удалить исходную папку: {e}")


# ===== РАСШИФРОВКА ПАПКИ (РАСШИФРОВКА АРХИВА + РАСПАКОВКА) =====
def decrypt_folder(filepath, password):
    if not filepath.endswith('.zip.enc'):
        raise Exception("Для папок выберите файл с расширением .zip.enc")

    # Расшифровываем .zip.enc -> получаем .zip файл обратно
    decrypt_file(filepath, password)
    zip_path = filepath.replace('.enc', '')

    # Целевая папка для распаковки (имя без .zip)
    output_folder = zip_path.replace('.zip', '')

    # Распаковываем архив обратно в папку
    try:
        shutil.unpack_archive(zip_path, output_folder, 'zip')
        # Удаляем временный расшифрованный zip-архив
        os.remove(zip_path)
    except Exception as e:
        raise Exception(f"Ошибка при распаковке архива: {e}")
