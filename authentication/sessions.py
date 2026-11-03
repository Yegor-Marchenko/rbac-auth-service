import hashlib
import secrets
from datetime import timedelta

from django.utils import timezone

from authentication.models import Session


def create_session(user):
    token = secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(token.encode('utf-8')).hexdigest()
    expires_at = timezone.now() + timedelta(days=7)

    Session.objects.create(
        user=user,
        session_key_hash=hashed_token,
        expires_at=expires_at
    )

    return token

