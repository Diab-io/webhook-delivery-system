import bcrypt

def hash_api_key(api_key: str) -> str:
        return bcrypt.hashpw(api_key.encode, bcrypt.gensalt()).decode()
    
def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    return bcrypt.checkpw(plain_key.encode(), hashed_key.encode())