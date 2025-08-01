import pathlib,secrets,base64,getpass
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from pathlib import Path

print("Script is running inside virtual environment!")

#password="Rabeelthecsstudent"    # We are not using this because of the argpase code at the buttom
#filename=""                      # This too
#foldername=""                     #This too

def generate_salt(size=16):
    return secrets.token_bytes(size)


def derive_key(salt,password):
    kdf=Scrypt(length=32,n=2**14,p=1,r=8,salt=salt)
    return kdf.derive(password.encode())
def load_salt():
    with open ("salt.salt",'rb') as f:
        return f.read()
    
def generate_key(password,size=16,):
    if pathlib.Path('salt.salt').exists():
        salt=load_salt()

    else:
        salt=generate_salt(size)
        with open("salt.salt","wb") as salt_file:
            salt_file.write(salt)
    
    derived_key=derive_key(salt,password)
    return base64.urlsafe_b64encode(derived_key)

def encrypt(filename,key):
    f=Fernet(key)
    with open(filename,'rb') as file:
        file_data=file.read()
        encrypted_data=f.encrypt(file_data)
        with open(filename,'wb') as file:
            file.write(encrypted_data) 
        print("File has been ecypted successfully")
            

#key=generate_key(password)     # We are not using this because of the folder encryption code at the buttom
#encrypt(filename,key)          # We are not using this because of the folder encryption code at the buttom

def decrypt(filename,key):
    f=Fernet(key)
    with open(filename,'rb') as file:
        file_data=file.read()


    try:
        decrypted_data=f.decrypt(file_data)
    except Exception as e:
        print(e)
        return

    with open(filename,'wb') as file:
        file.write(decrypted_data)
        print("file has been decrytped successfully ")

#key=generate_key(password)                 # We are not using this because of the folder encryption code at the buttom
#decrypt(filename,key)                        # We are not using this because of the folder encryption code at the buttom



#Now we need to learn how to decrypt and encrypt folder not just files 
def encrypt_folder(foldername,key):
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"Encrypting {child}")
            encrypt(child,key)
        elif child.is_dir():
            encrypt_folder(child,key)

def decrypt_folder(foldername,key):
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"Decrypting {child}")
            decrypt(child,key)
        elif child.is_dir():
            print(f"Decrypting {child}")
            decrypt_folder(child,key)
#key=generate_key(password)
#encrypt_folders(foldername,key)
#decrypt_folder(foldername,key)

import argparse
parser =argparse.ArgumentParser(description="File encryptor with a password")
parser.add_argument('path',help="Path to ecrypt or decrypt,and be a file or and entire folder")

parser.add_argument('-e',"--encrypt",action="store_true",help="whether to encrypt the file/folder.Only -e or -d can be specified")
parser.add_argument('-d',"--decrypt",action="store_true",help="whether to decrypt the file/folder.Only -e or -d can be specified")
args=parser.parse_args()

if args.encrypt:
    password=getpass.getpass("Enter the password for encryption ")
elif args.decrypt:
    password=getpass.getpass("Enter the password for decryption ")


encrypt_=args.encrypt
decrypt_=args.decrypt
target =Path(args.path)

if not target.exists():
    print(f"Filename or foldername {target} does not exist")
if encrypt_ and decrypt_:
    raise TypeError('Plase specify whether to decrypt or encrypt')
elif encrypt_:
    if target.is_file():
        key =generate_key(password)
        encrypt(filename=target,key=key)

        print("successfully encrytped")
    elif target.is_dir():
        key =generate_key(password)
        encrypt_folder(foldername=target,key=key)
        print("successfully encrytped")
elif decrypt_:
    if target.is_file():
        key =generate_key(password)
        decrypt(filename=target,key=key)
        print("successfully decrypted")
    elif target.is_dir():
        key =generate_key(password)
        decrypt_folder(foldername=target,key=key)
        print("successfully decrypted")
else:
    raise TypeError("Please specify whether to decrypt or encrypt")

