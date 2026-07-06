import base64


def encode_cursor(index: int) -> str:
    """Encode the next start index into an opaque cursor."""
    return base64.urlsafe_b64encode(str(index).encode()).decode()


def decode_cursor(cursor: str) -> int:
    """Decode cursor back to the start index."""
    return int(base64.urlsafe_b64decode(cursor.encode()).decode())