"""redis implementation"""

import socket  # noqa: F401


def main():
    """main function to start our redis journey"""
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        conn, _ = server_socket.accept()  # wait for client
        handle_conn(conn)


def handle_conn(conn):
    """connection handler"""
    while conn.recv(1024):
        conn.sendall(b"+PONG\r\n")
    conn.close()


if __name__ == "__main__":
    main()
