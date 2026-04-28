"""Client for the COMPX234 tuple space protocol."""

import os
import socket
import sys

from tuple_protocol import (
    MAX_KEY_VALUE_SIZE,
    ProtocolError,
    add_length_prefix,
    receive_framed_message,
    strip_length_prefix,
)

VALID_PORT_RANGE = range(50000, 60000)


class RequestFormatError(ValueError):
    """Raised when an input-file request line is not valid."""


def parse_port(text: str) -> int:
    try:
        port = int(text)
    except ValueError as exc:
        raise RequestFormatError("port must be an integer") from exc
    if port not in VALID_PORT_RANGE:
        raise RequestFormatError("port must be in the range 50000 to 59999")
    return port


def build_request(line: str) -> str:
    parts = line.split(" ", 2)
    command = parts[0]

    if command in {"READ", "GET"}:
        if len(parts) != 2 or not parts[1]:
            raise RequestFormatError(f"invalid {command} request")
        op = "R" if command == "READ" else "G"
        return add_length_prefix(f"{op} {parts[1]}")

    if command == "PUT":
        if len(parts) != 3 or not parts[1] or not parts[2]:
            raise RequestFormatError("invalid PUT request")
        key = parts[1]
        value = parts[2]
        if len(f"{key} {value}") > MAX_KEY_VALUE_SIZE:
            raise RequestFormatError("key and value exceed 970 characters")
        return add_length_prefix(f"P {key} {value}")

    raise RequestFormatError(f"unknown command {command}")


def run_client(hostname: str, port: int, input_file_path: str) -> None:
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((hostname, port))
            for raw_line in input_file:
                line = raw_line.strip()
                if not line:
                    continue

                try:
                    request = build_request(line)
                except (ProtocolError, RequestFormatError) as exc:
                    print(f"Invalid request skipped: {line} ({exc})")
                    continue

                sock.sendall(request.encode("utf-8"))
                response = receive_framed_message(sock)
                if response is None:
                    raise ConnectionError("server closed the connection")
                print(f"{line}: {strip_length_prefix(response)}")


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python TupleSpaceClient.py <server-hostname> <server-port> <input-file>")
        sys.exit(1)

    hostname = sys.argv[1]
    try:
        port = parse_port(sys.argv[2])
    except RequestFormatError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    input_file_path = sys.argv[3]
    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' does not exist.")
        sys.exit(1)

    try:
        run_client(hostname, port, input_file_path)
    except (OSError, ProtocolError, ConnectionError) as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
