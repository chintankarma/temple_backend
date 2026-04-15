import random

otp_store = {}

def generate_otp(mobile_no: str):
    otp = str(random.randint(1000, 9999))
    otp_store[mobile_no] = otp
    return otp

def verify_otp(mobile_no: str, otp: str):
    return otp_store.get(mobile_no) == otp