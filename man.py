import os
import hashlib


def convert_data_to_sha1(text):
    digest=hashlib.sha1(
        text.encode()
    ).hexdigest()

    return digest




def main():
    user_sha_1=input("Enter your password")
    cleaned_sha_1= user_sha_1.strip()
    file_path="password.txt"
    with open(file_path) as f:
        for line in f:
            password=line.strip()
            convert_sha1=convert_data_to_sha1(password)

            if cleaned_sha_1==convert_sha1:
                print(f"password found: {password}")
                return
    print("Could not find password")
    

if __name__=="__main__":
    main()