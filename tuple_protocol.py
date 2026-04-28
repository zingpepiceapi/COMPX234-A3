"""Protocol helpers for the COMPX234 tuple space assignment."""

MAX_MESSAGE_SIZE = 999
MAX_KEY_VALUE_SIZE = 970
MIN_MESSAGE_SIZE = 7


class ProtocolError(ValueError):
    """Raised when a protocol message cannot be encoded or decoded."""


def add_length_prefix(body: str) -> str:
    total_size = len(body) + 4
    if total_size > MAX_MESSAGE_SIZE:
        raise ProtocolError(f"message length {total_size} exceeds {MAX_MESSAGE_SIZE}")
    if total_size < MIN_MESSAGE_SIZE:
        raise ProtocolError(f"message length {total_size} is below {MIN_MESSAGE_SIZE}")
    return f"{total_size:03d} {body}"


def parse_length_prefix(prefix: bytes) -> int:
    if len(prefix) != 3:
        raise ProtocolError("incomplete length prefix")
    try:
        size = int(prefix.decode("ascii"))
    except UnicodeDecodeError as exc:
        raise ProtocolError("length prefix is not ASCII") from exc
    except ValueError as exc:
        raise ProtocolError("length prefix is not numeric") from exc
    if size < MIN_MESSAGE_SIZE or size > MAX_MESSAGE_SIZE:
        raise ProtocolError(f"message length {size} is outside valid range")
    return size


def receive_exactly(sock, byte_count: int) -> bytes:
    data = b""
    while len(data) < byte_count:
        chunk = sock.recv(byte_count - len(data))
        if not chunk:
            break
        data += chunk
    return data


def receive_framed_message(sock) -> str | None:
    prefix = receive_exactly(sock, 3)
    if not prefix:
        return None
    size = parse_length_prefix(prefix)
    remainder = receive_exactly(sock, size - 3)
    if len(remainder) != size - 3:
        raise ProtocolError("connection closed before full message arrived")
    return (prefix + remainder).decode("utf-8")


def strip_length_prefix(message: str) -> str:
    if len(message) < 4 or message[3] != " ":
        raise ProtocolError("message does not contain a length prefix separator")
    size = parse_length_prefix(message[:3].encode("ascii"))
    if len(message) != size:
        raise ProtocolError("message length does not match prefix")
    return message[4:]
