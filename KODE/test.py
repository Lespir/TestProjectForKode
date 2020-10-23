import random
from hashlib import sha256

# chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
#
#
# def key_gen():
#     password = ''
#
#     for i in range(10):
#         password += random.choice(chars)
#
#     return password
#
print(sha256(bytes('lespir', 'utf-8')).hexdigest())

