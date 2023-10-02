import os

user_api = input("Enter your api key: ")

if not os.path.isfile("userapikey.txt"):
    open("userapikey.txt", "x")

with open("userapikey.txt","w") as f:
    writekey = f.write(user_api)

