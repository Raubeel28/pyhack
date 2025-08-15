from cryptography.hazmat.primitives.asymmetric import rsa ,padding
from cryptography.hazmat.primitives import serialization,hashes

def generate_pair():
    private_key=rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key=private_key.public_key()

    password=("This is the password").encode()
    original_message=("This is the message we want to use ").encode()

    private_pem=private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password=password)

        )
    with open('private.pem','wb') as f:
        f.write(private_pem)

    public_pem=public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo

    )
    with open('public.pem','wb') as file:
        file.write(public_pem)

    loaded_private=serialization.load_pem_private_key(
        private_pem,
        password=password

    )
    loaded_public=serialization.load_pem_public_key(
        public_pem
    )
    #Encryption of the message
    encrypted_data=public_key.encrypt(
        original_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    decrypted_data=private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),  
            label=None      
            )

    )

    print(f"{encrypted_data}")
    print(f"{decrypted_data}")

generate_pair()
