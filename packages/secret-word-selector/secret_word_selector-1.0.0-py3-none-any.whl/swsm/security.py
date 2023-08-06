import base64
import pickle
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def crypto_key(password,salt):
    '''Create a Fernet key with user's password and salt.
        Use to encrypt and decrypt user secrets.'''
    b_password = password.encode('utf-8')
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                    length = 32,
                    salt = salt,
                    iterations = 100000)

    key = base64.urlsafe_b64encode(kdf.derive(b_password))
    f = Fernet(key)
    return f

def decrypt_secrets(config,key):
    '''get secrets from config and decrypt it with fernet key. unpickle the
        the decrypted secrets dictionary and return'''
    eenc = config.get('secrets','secrets')
    enc = eenc.encode('latin1')
    dec = key.decrypt(enc)
    secrets = pickle.loads(dec)
    return secrets

def encrypt_secrets(config,config_path,key,secrets):
    '''encrypt pickled secrets dictionary with fernet key and write
        to config file'''
    pickled = pickle.dumps(secrets)
    enc = key.encrypt(pickled)
    eenc = enc.decode('latin1')
    config['secrets']['secrets'] = eenc
    with open(config_path,'w',encoding='latin1') as cfg:
        config.write(cfg)