"""
Example how to decrypt whatsapp msgstore backups.
"""
from Crypto.Cipher import AES
import zlib
import sys

datafile = keyfile = None

if len(sys.argv)==1:
    print("Usage: decodecrypt12.py <keyfile> <msgstore.db.crypt12>")
    print("  the key file is commonly found in /data/data/com.whatsapp/files/key")
    print("  the crypt file is commonly found in the directory: /data/media/0/WhatsApp/Databases/")
    exit(1)

for arg in sys.argv[1:]:
    if arg.find('crypt12')>0:
        datafile = arg
    elif arg.find('key')>0:
        keyfile = arg
    else:
        keyfile = arg
        print("unknown arg", arg)

with open(keyfile, "rb") as fh:
   keydata = fh.read()
key = keydata[-32:]

with open(datafile, "rb") as fh:
   filedata = fh.read()
iv = filedata[51:67]

aes = AES.new(key, mode=AES.MODE_GCM, nonce=iv)

with open("msg-decrypted.db", "wb") as fh:
    fh.write(zlib.decompress(aes.decrypt(filedata[67:-20])))

