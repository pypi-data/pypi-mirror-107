from pyrasgo.api.register import Register
from pyrasgo.schemas.user import UserRegistration, UserLogin

from urllib.error import HTTPError

__all__ = [
    'connect',
    'orchestrate', 
    'register',
    'login'
]

def connect(api_key):
    from pyrasgo.rasgo import Rasgo
    return Rasgo(api_key=api_key)

def orchestrate(api_key):
    from pyrasgo.orchestration import RasgoOrchestration
    return RasgoOrchestration(api_key=api_key)

def register(email: str, password: str):
    register = Register()
    payload = UserRegistration(
        email=email,
        password=password
    )
    register.register(payload=payload)
    print(f"Verification Email Sent to {email}. To ensure uninterrupted access, please finish setting up your free Rasgo account by clicking the verification link in the next 24 hours")
    
def login(email: str, password: str):
    register = Register()
    payload = UserLogin(
        email=email,
        password=password
    )
    response = register.login(payload=payload)
    return connect(api_key=response)
