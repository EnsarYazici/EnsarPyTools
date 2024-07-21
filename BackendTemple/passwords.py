import bcrypt

# Şifreyi hash'leme
password = "otuzbirci"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed)
# Şifreyi doğrulama
if bcrypt.checkpw(password, hashed):
    print("Şifre doğru!")
else:
    print("Şifre yanlış!")
