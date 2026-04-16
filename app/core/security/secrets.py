import bcrypt
import secrets

def hash_api_key(api_key: str) -> str:
        return bcrypt.hashpw(api_key.encode(), bcrypt.gensalt()).decode()
    
def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    return bcrypt.checkpw(plain_key.encode(), hashed_key.encode())

def generate_api_key() -> str:
    return f"sk_" + secrets.token_hex(4)

def generate_webhook_secret():
       return "whsec_" + secrets.token_urlsafe(32)