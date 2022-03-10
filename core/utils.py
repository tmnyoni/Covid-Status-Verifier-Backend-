import hmac
import hashlib
import binascii
from decouple import config


def generate_hmac_code(message):
    ''' 
    Generates hmac code.

    @param message:
    message to be hashed.
    '''
    key = binascii.unhexlify(config("QRCODE_KEY"))
    return hmac.new(
        key,
        message.encode(),
        hashlib.sha3_512
    ).hexdigest().upper()
