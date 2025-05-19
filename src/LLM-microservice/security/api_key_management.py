from flask import request, abort
import os

def require_api_key(func):
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            # Allow preflight requests without API Key validation
            return func(*args, **kwargs)
        
        client_key = request.headers.get("x-api-key")
        server_key = os.getenv("API_KEY")

        if client_key != server_key:
            abort(401, description="Unauthorized: Invalid API Key")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # for Flask to recognize the function name
    return wrapper
