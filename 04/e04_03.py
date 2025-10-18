import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from cryptography.fernet import Fernet
    from time import perf_counter as pfc


    mo.md("# Библиотека cryptography")
    return Fernet, mo, pfc


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Fernet
    ### Создаем ключ
    """
    )
    return


@app.cell
def _(Fernet):
    key = Fernet.generate_key()
    print(f"Ключ: {key}")
    return (key,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Подгружаем "Уловку 22"
    """
    )
    return


@app.cell
def _():
    with open("./texts/catch22.txt", "r", encoding="utf-8") as f:
        catch22 = f.read()
    len(catch22)
    return (catch22,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Зашифровываем / расшифровываем  "Уловку 22"
    """
    )
    return


@app.cell
def _(Fernet, catch22, key, pfc):
    _time_stamp = pfc()
    # Создание объекта шифрования
    _token = Fernet(key)
    # Зашифровываем
    _encrypted_text = _token.encrypt(catch22.encode())
    # расшифровываем, не забывая раскодировать текст
    _decrypted_text = _token.decrypt(_encrypted_text).decode()
    _elapsed_time = pfc() - _time_stamp

    print(f'Длина открытого текста: {len(catch22)}')
    print(f"Длина зашифрованного текста: {len(_encrypted_text)}")
    print(f"Первые 100 символов зашифрованного текста: \n{_encrypted_text[:100]}")
    print(f'Успешность зашифровки/расшифровки "Уловки 22": {catch22==_decrypted_text }')
    print(f'Время зашифровки/расшифровки "Уловки 22": {_elapsed_time:6.3e}')
    _decrypted_text
    return


@app.cell
def _(mo):
    mo.md(r"""### Контроль времени жизни сообщений (TTL)""")
    return


@app.cell
def _(Fernet, catch22, key):
    # Создание объекта шифрования
    import time
    _token = Fernet(key)
    _encrypted_text = _token.encrypt(catch22.encode())
    _ttl = 3
    time.sleep(_ttl + 1)

    # Проверка времени жизни сообщения
    try:
        # время жизни (ttl) 60 секунд
        _decrypted_text = _token.decrypt(_encrypted_text, ttl=_ttl).decode()
        print("Сообщение расшифровано ранее завершения срока действия")
        print(f'Успешность зашифровки/расшифровки "Уловки 22": {catch22==_decrypted_text }')
    except:
        print("Сообщение устарело")    
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Асимметричное шифрование. Алгоритм RSA 
    ### Генерация пары ключей
    """
    )
    return


@app.cell
def _():
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend

    # секретный ключ
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096, #2048,
        backend=default_backend(),
    )

    # Получение публичного ключа
    public_key = private_key.public_key()
    return default_backend, private_key, public_key, rsa, serialization


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Сериализация / десериализация ключей RSA""")
    return


@app.cell
def _(default_backend, private_key, public_key, serialization):
    # Сериализация секретного ключа
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Сохранение секретного ключа в файловой системе
    with open('private_key.pem', 'wb') as _f:
        _f.write(private_pem)

    # Сериализация открытого ключа
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Сохранение открытого ключа в файловой системе
    with open('public_key.pem', 'wb') as _f:
        _f.write(public_pem)

    # Чтение ключей из файловой системы

    with open("private_key.pem", "rb") as _f:
        loaded_private_key = serialization.load_pem_private_key(
            _f.read(),
            password=None,
            backend=default_backend(),
        )

    with open("public_key.pem", "rb") as _f:
        loaded_public_key = serialization.load_pem_public_key(
            _f.read(),
            backend=default_backend()
        )

    print(f"Секретный ключ: \n{private_pem}") 
    print(f"Открытый ключ: \n{public_pem}") 
    return loaded_private_key, loaded_public_key


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Зашифрование / расшифрование
    Зашифровать можно только короткие тексты
    """
    )
    return


@app.cell
def _(catch22, loaded_private_key, loaded_public_key, pfc):
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes

    _time_stamp = pfc()
    # Зашифрование
    _n = 200
    text = catch22[:_n]
    _text = text.encode()
    # зашифровываем  на открытом ключе, расшифровывем на секретном
    _encrypted_text = loaded_public_key.encrypt(
        _text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # расшифровка
    _decrypted_text= loaded_private_key.decrypt(
        _encrypted_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()


    _elapsed_time = pfc() - _time_stamp
    print(f"Проверяем корректность работы RSA")
    print(f"{text==_decrypted_text=}")
    print(f"Время работы: {_elapsed_time:6.3e} c")
    return hashes, padding


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Вычисляем хеш для "Уловки 22"
    """
    )
    return


@app.cell
def _(catch22, hashes, pfc):
    #from cryptography.hazmat.primitives import hashes
    import base64

    catch22_ = catch22 + '_' # доавляю символ
    bcatch22 = bytes(catch22, encoding='utf-8')
    bcatch22_ = bytes(catch22_, encoding='utf-8')

    # Создание объектов хеша
    _time_stamp = pfc()
    digest = hashes.Hash(hashes.SHA256())
    digest_ = hashes.Hash(hashes.SHA256())
    digest.update(bcatch22)
    digest_.update(bcatch22_)
    _time_elapsed = pfc() - _time_stamp
    print(f"Хеш catch22:  {base64.b64encode(digest.copy().finalize())}")
    print(f"Хеш catch22_: {base64.b64encode(digest_.copy().finalize())}")
    print(f"Время вычисления хешей: {_time_elapsed:6.3e}")
    base64.b64encode(digest.copy().finalize()), base64.b64encode(digest_.copy().finalize())
    len(digest.copy().finalize()), len(digest_.copy().finalize())
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Асимметричное шифрование. Эллиптические кривые""")
    return


@app.cell
def _(catch22, hashes):
    from cryptography.hazmat.primitives.asymmetric import ec

    # Генерация ключа на кривой SECP256R1
    _private_key = ec.generate_private_key(ec.SECP256R1())
    _public_key = _private_key.public_key()

    # Подпись
    message_2_sign = bytes("Сообщение для подписи", encoding='utf-8')
    message_2_sign =  bytes(catch22, encoding='utf-8')
    _signature = _private_key.sign(
        message_2_sign,
        ec.ECDSA(hashes.SHA256())
    )

    # Проверка подписи
    try:
        _public_key.verify(_signature, message_2_sign, ec.ECDSA(hashes.SHA256()))
        print("Подпись верна")
    except Exception as ex:
        print(f"Подпись неверна: {ex}")
    print(_signature, '\n', len(_signature))
    _private_key.key_size
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Алиса пересылает Бобу зашифрованную "Уловку 22"
    ### Алиса и Боб создают секретные и открытые ключи
    """
    )
    return


@app.cell
def _(default_backend, rsa, serialization):
    from cryptography.hazmat.primitives.serialization import load_pem_public_key

    def generate_rsa_keys(name, key_size=4096):
        '''
        Генерация и сериализация ключей RSA
        Параметры:
        name - имя участника
        key_size - длина ключа в битах 
        Функция возращает:
        секретный и отрытый ключи
        сериализованные секретные и открытые ключи
        Примечание:
        сериализованные секретные и открытые ключи
        записываются в текущую папку
        '''
        # секретный ключ
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size, 
            backend=default_backend(),
        )  

        # открытый ключ
        public_key = private_key.public_key()

        # сериализация и запись секретного ключа в файловую систему
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(name + '_private_key.pem', 'wb') as _f:
            _f.write(private_pem)


        # сериализация и запись открытого ключа в файловую систему
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(name + '_public_key.pem', 'wb') as _f:
            _f.write(public_pem) 

        return private_key, public_key, private_pem, public_pem

    def load_public_key(name):
        '''
        Загрузка из файловой системы сериализованного
        открытого ключа и пренобразование его в открытый
        ключ
        Параметры:
        name - имя участника
        Функция возвращает открытый ключ участника
        '''
        with open(name + "_public_key.pem", "rb") as f:
            pem_data = f.read()   

        public_key = load_pem_public_key(pem_data)
        return public_key


    (alice_private_key, alice_public_key, 
     alice_private_pem, alice_public_pem) = generate_rsa_keys('alice')

    # Алиса пересылает alice_public_pem Бобу, например, по электронной почте
    return (
        alice_private_key,
        alice_public_key,
        generate_rsa_keys,
        load_public_key,
    )


@app.cell
def _(generate_rsa_keys, load_public_key):
    # Боб создает пару ключей

    (bob_private_key, bob_public_key, 
     bob_private_pem, bob_public_pem) = generate_rsa_keys('bob')

    # Боб загружает присанный Алисой открытый ключ
    alice_public_key_ = load_public_key('alice')

    # Боб пересылает bob_public_pem Алису, например, по электронной почте
    return bob_private_key, bob_public_key


@app.cell
def _(load_public_key):
    # Алиса загружает присланный Бобом открытый ключ
    bob_public_key_ = load_public_key('bob')
    return


@app.cell
def _(Fernet, catch22, hashes):
    # Алиса генерирует одноразовый сессионный ключ
    session_key = Fernet.generate_key()

    # Алиса зашифровывает "Уловку 22" одноразовым ключом
    # Создание объекта шифрования
    _token = Fernet(session_key)
    # Зашифровываем "Уловку 22"
    encrypted_catch22 = _token.encrypt(catch22.encode())

    # Создаем хеш  зашифрованной "Уловки 22"
    _hash = hashes.Hash(hashes.SHA256())
    _hash.update(encrypted_catch22)
    catch22_hash = _hash.finalize()
    catch22_hash
    return catch22_hash, encrypted_catch22, session_key


@app.cell
def _(alice_private_key, catch22_hash, hashes, padding):
    # Алиса подписывает хеш "Уловки 22" своим секретным ключом
    catch22_signature = alice_private_key.sign(
        catch22_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Хеш сообщения подписывается секретным ключом Алисы. Это гарантирует, что сообщение не было изменено 
    # и его отправила именно Алиса - владелица  секретного ключа. 

    catch22_signature
    return (catch22_signature,)


@app.cell
def _(bob_public_key, hashes, padding, session_key):
    # Алиса шифрует одноразовый сессионный ключ. 
    encrypted_session_key = bob_public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # Одноразовый сессионный ключ шифруется открытым ключом Боба. Только Боб, 
    # имеющий соответствующий секретный ключ, сможет его расшифровать.
    encrypted_session_key
    return (encrypted_session_key,)


@app.cell
def _(mo):
    mo.md(
        r"""
    Все готово. Алиса отсылает Бобу любым доступным ей способом: 

    - encrypted_catch22 - зашифрованную на одноразовом сессионном ключе "Уловку 22";
    - encrypted_session_key - зашифрованный на открытом ключе Алисы сессионный ключ;
    - catch22_hash - хеш передаваемого сообщения ("Уловка-22");
    - catch22_signature - подпись открытым ключом Боба хеша "Уловки-22"

    Получив, присланные Алисой объекты, Боб осуществляет следующие действия:
    """
    )
    return


@app.cell
def _(bob_private_key, encrypted_session_key, hashes, padding):
    # Боб расшифровывает сессионный ключ своим секретным ключом. 
    # Использование секретного ключа гарантирует, что сделать это может только Боб 
    decrypted_session_key = bob_private_key.decrypt(
        encrypted_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    decrypted_session_key
    return (decrypted_session_key,)


@app.cell
def _(
    Fernet,
    alice_public_key,
    catch22,
    catch22_hash,
    catch22_signature,
    decrypted_session_key,
    encrypted_catch22,
    hashes,
    padding,
):
    # Боб проверяет, что  переданное сообщение не изменено. 
    # Для этого необходимо вычислить хеш переданного сообщения и проверить 
    # подпись с помощью открытого ключа Алисы. 
    # Если проверка не пройдет, будет возбуждено исключение. 

    try:
        # Проверка подписи с использованием открытого ключа Алисы
        alice_public_key.verify(
            catch22_signature,
            catch22_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Подпись действительна. Сообщение не было изменено.")
        # Теперь можно расшифровать зашифрованную "Уловку 22"
        # на сессионном ключе.
        _token = Fernet(decrypted_session_key)
        # расшифровываем, не забывая раскодировать текст
        decrypted_catch22 = _token.decrypt(encrypted_catch22).decode()
        if catch22 == decrypted_catch22:
            print('Исходный и расшифрованный тексты "Уловки 22" совпадают.')
        else:
            print("Произошла ошибка. Исходный и расшифрованный тексты не совпадают.")

    except Exception as e:
        print(f"Ошибка проверки подписи: {e}")
    return


@app.cell
def _(mo):
    mo.md(r"""## Сертификат X.509""")
    return


@app.cell
def _(alice_public_key, hashes, private_key, rsa):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    import datetime

    # Один день - интервал времени
    one_day = datetime.timedelta(1, 0, 0)

    # Ключи выпускающего сертификат
    issuer_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    issuer_public_key = private_key.public_key()

    # Выпуск сертификата
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, 'Алиса'),
    ]))
    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, 
                           'horns_n_hoofs.com'),
    ]))

    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 90))
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(alice_public_key)
    builder = builder.add_extension(
        x509.SubjectAlternativeName(
            [x509.DNSName('horns_n_hoofs.com')]
        ),
        critical=False 
    )
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )
    certificate = builder.sign(
        private_key=issuer_private_key, algorithm=hashes.SHA256(),
    )
    print("Является ли сертификат сертификатом X.509:", isinstance(certificate, x509.Certificate))
    return (certificate,)


@app.cell
def _(certificate):
    print(f"Владелец сертификата: {certificate.subject}")
    print(f"Начало действия сертификата: {certificate.not_valid_before_utc}")
    print(f"Конец действия сертификата: {certificate.not_valid_after_utc}")
    print("Организация/лицо, выпустившая сертификат:",
         certificate.issuer)
    print(f"Открытый ключ владельца сертификата:",
         certificate.public_key())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    С помощью библиотеки cryptography в Python можно зашифровать и подписать данные, используя алгоритм RSA, и затем проверить подпись и расшифровать их.

    В этом процессе обычно используется гибридное шифрование: RSA для шифрования сессионного ключа (симметричного), а затем этот ключ для шифрования самих данных. Подпись же создается с помощью хеша сообщения, подписанного закрытым ключом.
    ##1. Генерация ключей и данных 🔑

    Сначала нужно сгенерировать пару RSA-ключей (публичный и закрытый) и сессионный ключ AES, а также исходное сообщение.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ```python
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import os

    # 1. Генерация RSA-ключей
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 2. Генерация сессионного ключа AES и вектора инициализации (IV)
    session_key = os.urandom(32)  # 256 бит
    iv = os.urandom(16)            # 128 бит

    # 3. Исходное сообщение
    message = b"This is a secret message."

    # 4. Хеширование сообщения
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(message)
    message_hash = hasher.finalize()
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ##2. Шифрование и подписание 🔒

    На этом этапе мы шифруем сессионный ключ и подписываем хеш сообщения.

    Подписание хеша сообщения

    Хеш сообщения подписывается закрытым ключом отправителя. Это гарантирует, что сообщение не было изменено и его отправил именно владелец закрытого ключа.
    ```python
    # Подписание хеша сообщения закрытым ключом
    signature = private_key.sign(
        message_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ###Шифрование сессионного ключа

    Сессионный ключ шифруется публичным ключом получателя. Только получатель, имеющий соответствующий закрытый ключ, сможет его расшифровать.

    ```python
    # Шифрование сессионного ключа публичным ключом
    encrypted_session_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ##3. Расшифровка и проверка 🔓

    Получатель получает зашифрованный сессионный ключ, подпись и исходное сообщение (предполагается, что оно было передано отдельно и зашифровано сессионным ключом).

    ###Расшифровка сессионного ключа

    Сессионный ключ расшифровывается закрытым ключом получателя.
    ```Python
    # Расшифровка сессионного ключа закрытым ключом
    decrypted_session_key = private_key.decrypt(
        encrypted_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    ```
    ### Проверка подписи

    Для проверки подписи необходимо снова вычислить хеш сообщения и проверить, что подпись совпадает с хешем, используя публичный ключ отправителя. Если проверка не пройдет, будет вызвано исключение.
    ```Python
    try:
        # Проверка подписи с использованием публичного ключа
        public_key.verify(
            signature,
            message_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Подпись действительна. Сообщение не было изменено.")
    except Exception as e:
        print(f"Ошибка проверки подписи: {e}")
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    С помощью библиотеки **`cryptography`** в Python можно зашифровать и подписать данные, используя алгоритм **RSA**, и затем проверить подпись и расшифровать их.

    В этом процессе обычно используется гибридное шифрование: RSA для шифрования **сессионного ключа** (симметричного), а затем этот ключ для шифрования самих данных. Подпись же создается с помощью хеша сообщения, подписанного **закрытым ключом**.

    -----

    ### 1\. Генерация ключей и данных 🔑

    Сначала нужно сгенерировать пару RSA-ключей (публичный и закрытый) и сессионный ключ AES, а также исходное сообщение.

    ```python
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import os

    # 1. Генерация RSA-ключей
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 2. Генерация сессионного ключа AES и вектора инициализации (IV)
    session_key = os.urandom(32)  # 256 бит
    iv = os.urandom(16)            # 128 бит

    # 3. Исходное сообщение
    message = b"This is a secret message."

    # 4. Хеширование сообщения
    hasher = hashes.Hash(hashes.SHA256())
    hasher.update(message)
    message_hash = hasher.finalize()
    ```

    -----

    ### 2\. Шифрование и подписание 🔒

    На этом этапе мы шифруем сессионный ключ и подписываем хеш сообщения.

    #### **Подписание хеша сообщения**

    Хеш сообщения подписывается **закрытым ключом** отправителя. Это гарантирует, что сообщение не было изменено и его отправил именно владелец закрытого ключа.

    ```python
    # Подписание хеша сообщения закрытым ключом
    signature = private_key.sign(
        message_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    ```

    #### **Шифрование сессионного ключа**

    Сессионный ключ шифруется **публичным ключом** получателя. Только получатель, имеющий соответствующий закрытый ключ, сможет его расшифровать.

    ```python
    # Шифрование сессионного ключа публичным ключом
    encrypted_session_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    ```

    -----

    ### 3\. Расшифровка и проверка 🔓

    Получатель получает зашифрованный сессионный ключ, подпись и исходное сообщение (предполагается, что оно было передано отдельно и зашифровано сессионным ключом).

    #### **Расшифровка сессионного ключа**

    Сессионный ключ расшифровывается **закрытым ключом** получателя.

    ```python
    # Расшифровка сессионного ключа закрытым ключом
    decrypted_session_key = private_key.decrypt(
        encrypted_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    ```

    #### **Проверка подписи**

    Для проверки подписи необходимо снова вычислить хеш сообщения и проверить, что подпись совпадает с хешем, используя **публичный ключ** отправителя. Если проверка не пройдет, будет вызвано исключение.

    ```python
    try:
        # Проверка подписи с использованием публичного ключа
        public_key.verify(
            signature,
            message_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Подпись действительна. Сообщение не было изменено.")
    except Exception as e:
        print(f"Ошибка проверки подписи: {e}")
    ```
    """
    )
    return


if __name__ == "__main__":
    app.run()
