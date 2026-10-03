# Import the standard library secrets helper for unpredictable CSRF tokens.
import secrets

# Import FastAPI's HTTP exception type.
from fastapi import HTTPException, Request, status

# Import password hashing utilities.
from passlib.context import CryptContext


# Configure bcrypt password hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash a plain-text administrator password.
def hash_password(password: str) -> str:
    # Return the secure password hash.
    return pwd_context.hash(password)


# Verify a password against its stored hash.
def verify_password(password: str, password_hash: str) -> bool:
    # Return whether the supplied password is valid.
    return pwd_context.verify(password, password_hash)


# Return the currently authenticated administrator or None.
def get_current_admin(request: Request):
    # Read the signed admin user ID from the session.
    return request.session.get("admin_user_id")


# Require an authenticated administrator for an admin route.
def require_admin(request: Request):
    # Read the signed administrator ID from the session.
    admin_id = get_current_admin(request)
    # Reject the request when no administrator session exists.
    if not admin_id:
        # Redirect-style authentication is handled by the route itself.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Return the authenticated administrator ID.
    return int(admin_id)


# Create and store a CSRF token in the signed session.
def ensure_csrf_token(request: Request) -> str:
    # Reuse an existing token for the current session when present.
    token = request.session.get("csrf_token")
    # Generate a new unpredictable token when needed.
    if not token:
        # Generate a URL-safe random token.
        token = secrets.token_urlsafe(32)
        # Store the token in the signed session.
        request.session["csrf_token"] = token
    # Return the token for the HTML form.
    return token


# Validate a submitted CSRF token against the session token.
def validate_csrf(request: Request, token: str | None):
    # Read the expected token from the signed session.
    expected = request.session.get("csrf_token")
    # Reject missing or mismatched tokens.
    if not token or not expected or not secrets.compare_digest(token, expected):
        # Return a standard forbidden response.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token.")
