import random
import string

def generateOTP(length=6) -> str:
    return "".join(random.choices(string.digits, k=length))
