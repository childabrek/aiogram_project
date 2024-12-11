from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
TOKEN = f.encrypt()
print(TOKEN)
d = f.decrypt(TOKEN)
print(d)