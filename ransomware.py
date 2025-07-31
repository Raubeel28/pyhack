import pathlib,secrets,base64,getpass
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

print("Script is running inside virtual environment!")

password="Rabeelthecsstudent"
filename="C:/Users/USER/Documents/summanry1.pdf"

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

#def encrypt(filename,key):
   # f=Fernet(key)
   # with open(filename,'rb') as file:
    #    file_data=file.read()
    #    encrypted_data=f.encrypt(file_data)
     #   with open(filename,'wb') as file:
      #      file.write(encrypted_data) 
       # print("File has been ecypted successfully")
            

#key=generate_key(password)
#encrypt(filename,key)

#def decrypt(filename,key):
 #   f=Fernet(key)
 #   with open(filename,'rb') as file:
 #       file_data=file.read()


  #  try:
   #     decrypted_data=f.decrypt(file_data)
   # except Exception as e:
   #     print(e)
   #     return

   # with open(filename,'wb') as file:
   #     file.write(decrypted_data)
   #     print("file has been decrytped successfully ")

#key=generate_key(password)
#decrypt(filename,key)
