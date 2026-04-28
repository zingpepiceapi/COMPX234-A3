"""Multithreaded tuple space server for COMPX234."""

import socket
import sys
import threading
import time

from tuple_protocol import (
    MAX_KEY_VALUE_SIZE,
    ProtocolError,
    add_length_prefix,
    receive_framed_message,
    strip_length_prefix,
)

VALID_PORT_RANGE = range(50000, 60000)


tuple_space: dict[str, str] = {}
stats = {
    "total_clients": 0,
    "total_operations": 0,
    "read_count": 0,
    "get_count": 0,
    "put_count": 0,
    "error_count": 0,
}
lock = threading.Lock()


def parse_port(text: str) -> int:
    try:
        port = int(text)
    except ValueError as exc:
        raise ValueError("port must be an integer") from exc
    if port not in VALID_PORT_RANGE:
        raise ValueError("port must be in the range 50000 to 59999")
    return port


def increment_stat(name: str) -> None:
    stats[name] += 1


def format_stats() -> str:
    tuple_count = len(tuple_space)
    avg_key_size = 0.0
    avg_value_size = 0.0
    avg_tuple_size = 0.0

    if tuple_count > 0:
        total_key_size = sum(len(key) for key in tuple_space)
        total_value_size = sum(len(value) for value in tuple_space.values())
        avg_key_size = total_key_size / tuple_count
        avg_value_size = total_value_size / tuple_count
        avg_tuple_size = avg_key_size + avg_value_size

    return (
        "\n--- Tuple Space Stats ---\n"
        f"Tuples: {tuple_count}\n"
        f"Avg Tuple Size: {avg_tuple_size:.2f}\n"
        f"Avg Key Size: {avg_key_size:.2f}\n"
        f"Avg Value Size: {avg_value_size:.2f}\n"
        f"Clients: {stats['total_clients']}\n"
        f"Operations: {stats['total_operations']}\n"
        f"READs: {stats['read_count']}\n"
        f"GETs: {stats['get_count']}\n"
        f"PUTs: {stats['put_count']}\n"
        f"Errors: {stats['error_count']}\n"
    )


def print_stats_forever() -> None:
    while True:
        time.sleep(10)
        with lock:
            print(format_stats(), flush=True)


def handle_request(body: str) -> str:
    parts = body.split(" ", 2)
    if len(parts) < 2:
        with lock:
            increment_stat("total_operations")
            increment_stat("error_count")
        return "ERR Invalid message"

    op = parts[0]
    key = parts[1]

    with lock:
        increment_stat("total_operations")

        if op == "R":
            increment_stat("read_count")
            if key in tuple_space:
                return f"OK ({key}, {tuple_space[key]}) read"
            increment_stat("error_count")
            return f"ERR {key} does not exist"

        if op == "G":
            increment_stat("get_count")
            value = tuple_space.pop(key, None)
            if value is not None:
                return f"OK ({key}, {value}) removed"
            increment_stat("error_count")
            return f"ERR {key} does not exist"

        if op == "P":
            increment_stat("put_count")
            if len(parts) < 3 or not parts[2]:
                increment_stat("error_count")
                return "ERR Invalid PUT"

            value = parts[2]
            if len(value) > 999 or len(f"{key} {value}") > MAX_KEY_VALUE_SIZE:
                increment_stat("error_count")
                return "ERR Invalid PUT"
            if key in tuple_space:
                increment_stat("error_count")
                return f"ERR {key} already exists"

            tuple_space[key] = value
            return f"OK ({key}, {value}) added"

        increment_stat("error_count")
        return "ERR Unknown operation"


def handle_client(client_socket: socket.socket, address) -> None:
    with lock:
        increment_stat("total_clients")
    try:
        while True:
            framed_message = receive_framed_message(client_socket)
            if framed_message is None:
                break
            body = strip_length_prefix(framed_message)
            response = add_length_prefix(handle_request(body))
            client_socket.sendall(response.encode("utf-8"))
    except (OSError, ProtocolError):
        pass
    finally:
        client_socket.close()
        print(f"Connection from {address} closed.", flush=True)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python TupleSpaceServer.py <port>")
        sys.exit(1)

    try:
        port = parse_port(sys.argv[1])
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen()
    print(f"Server started on port {port}", flush=True)

    stats_thread = threading.Thread(target=print_stats_forever, daemon=True)
    stats_thread.start()

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address} accepted.", flush=True)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down server...", flush=True)
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
