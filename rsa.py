def generate_keys(public_fname="public.pem", private_fname="private.pem"):
    # generate the key pair
    key = RSA.generate(2048)

    # ======= public key =======
    pub = key.public_key()
    pub_pem = pub.export_key(format='PEM')
    
    f = open(public_fname, 'wb')
    f.write(pub_pem)
    f.close()

    # ======= private key =======
    pem = key.export_key(format='PEM')

    f = open(private_fname, 'wb')
    f.write(pem)
    f.close()

# Encrypt a message using a public key
def encrypt_message(message, pub_key_path, out_fname="encrypted.txt"):
    f = open(out_fname, 'wb')

    key = RSA.importKey(open(pub_key_path).read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(message)

    f.write(ciphertext)
    f.close()
    
# Decrypt a message using a private key
def decrypt_message(message, priv_key_path, out_fname="decrypted.txt"):