import hashlib
import os

def hash_password(password):
    # Generate a random salt
    salt = b'wlstr'
    # Hash the password with the salt using PBKDF2-HMAC-SHA256
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Store the salt and the key together
    stored_password = salt + key
    # Return the stored password
    return stored_password.hex()

if __name__ == '__main__':
    password = 'passord123'
    hashed_password = hash_password(password)
    print(f'Hashed password: {hashed_password} \n')
    again = hash_password(password)
    print(f'Hashed password: {again}')