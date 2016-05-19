#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'binpo'

# easy_install rsa

from Crypto.Hash import SHA

import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import rsa

# load公钥和密钥


# (pubkey, privkey) = rsa.newkeys(1024)
# pub = pubkey.save_pkcs1()
# pubfile = open('public.pem','w+')
# pubfile.write(pub)
# pubfile.close()
# #
# pri = privkey.save_pkcs1()
# prifile = open('private.pem','w+')
# prifile.write(pri)
# prifile.close()

import os
current_path = os.path.dirname(__file__)
message = 'hello'

#
with open('rsa_private_key_pkcs8.pem','rb') as privatefile:
    key = privatefile.read()
    rsakey = RSA.importKey(key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message)
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)

     # p = privatefile.read()
     # privkey = rsa.PrivateKey.load_pkcs1(p)
     # signature = base64.b64encode(rsa.sign(message, privkey, 'SHA-1'))

with open('rsa_public_key.pem','rb') as publickfile:

    key = publickfile.read()
    rsakey = RSA.importKey(key)
    verifier = PKCS1_v1_5.new(rsakey)
    digest = SHA.new()
        # Assumes the data is base64 encoded to begin with
    digest.update(message)
    is_verify = verifier.verify(digest, base64.b64decode(signature))
    print is_verify





#     p = publickfile.read()
# #p='MIIDhzCCAm+gAwIBAgIGASYgtFQUMA0GCSqGSIb3DQEBBQUAMF8xCzAJBgNVBAYTAkNOMSkwJwYDVQQKDCBBbGxpbnBheSBOZXR3b3JrIFNlcnZpY2VzIENvLkx0ZDElMCMGA1UECwwcQWxsaW5wYXkgUHJpbWFyeSBDZXJ0aWZpY2F0ZTAeFw0xMDAxMTIwNDA0MzNaFw0zMDAxMDcwNDA0MzNaMGQxCzAJBgNVBAYTAkNOMSkwJwYDVQQKDCBBbGxpbnBheSBOZXR3b3JrIFNlcnZpY2VzIENvLkx0ZDEqMCgGA1UECwwhQWxsaW5wYXkgRGlnaXRhbCBTaWduIENlcnRpZmljYXRlMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUucCNCbCM2KGIRrR+MuzxdBwcsEdIlP+bkP50yufEiIHqAGKleCFIQVhVi23TGEqAcHb1FCOE6RBdXc/E9cfBBYuwfSu6RA50FABJhXBW3aS546tmyaTfOLHOKR+NvFe8Q2cRb+jRKJCP2MGxGpBxifXcfJ1pTFLSWE3DngR96wIDAQABo4HHMIHEMB0GA1UdDgQWBBSmPlA9zXUf5QUXm3bRwDbJXMd1CzCBjgYDVR0jBIGGMIGDgBRkngYunj9vGVSczC9heuKlAX9yZaFjpGEwXzELMAkGA1UEBhMCQ04xKTAnBgNVBAoMIEFsbGlucGF5IE5ldHdvcmsgU2VydmljZXMgQ28uTHRkMSUwIwYDVQQLDBxBbGxpbnBheSBQcmltYXJ5IENlcnRpZmljYXRlggYBJiC0U2AwEgYDVR0TAQH/BAgwBgEB/wIBADANBgkqhkiG9w0BAQUFAAOCAQEAK13MKF5lMKy9tNHYW6bkJWkQcwf39qLagcmkRGZVoSWE8E/2hyDoUP4PYcvxwpx+jA0L4FfAabfpO1VfWP/Cm6k+6NL/zcXKpES/kZfSXcThbTPvH1X2K87/QD0Wzse1dw6+UZbngEEst9MyKLjDrWd8wH3e6RNHZ4khEOE4zxvEKH9Q/fFhIjr+HTmv8LfTS4knR/TSQvBPf/qf4rBPl3lRhR5J4bYt3jQiwl+9vJGYVINCyBI2GwxMCFjgpZka96W6Y5CnjijvCoKG+ZanZY8xr8S4Yp1eZymgtGZ5YbUGp8OTplTlLtfNd06H1WEcdNbeunaYRYLqCHBBKkJjlg=='
#     pubkey = rsa.PublicKey.load_pkcs1(p)
#     try:
#     is_verify = rsa.verify(message,base64.b64decode(signature),pubkey)
#     except Exception,e:
#         is_verify = False
#
#     print is_verify








# 用公钥加密、再用私钥解密
# crypto = rsa.encrypt('1212121', pubkey)
# tr_result = base64.b64encode(crypto)
# message = rsa.decrypt(crypto, privkey)

# # sign 用私钥签名认真、再用公钥验证签名




