import unittest
import socket
from threading import Thread
from main import main

class TestHttpServer(unittest.TestCase):
    def setUp(self):
        self.server_thread = Thread(target=main)
        self.server_thread.daemon = True
        self.server_thread.start()
        import time

        time.sleep(1)

    def test_root_path(self):
        with socket.create_connection(("localhost", 6379), timeout=1) as client_socket:
            client_socket.sendall(b"*1\r\n$4\r\nping\r\n")
            response = client_socket.recv(1024)
            self.assertEqual(response, b"+PONG\r\n")

    # def test_not_found_path(self):
    #     with socket.create_connection(("localhost", 4221), timeout=1) as client_socket:
    #         client_socket.sendall(b"GET /notfound HTTP/1.1\r\n\r\n")
    #         response = client_socket.recv(1024)
    #         self.assertEqual(response, b"HTTP/1.1 404 Not Found\r\n\r\n")

    # def test_echo_path(self):
    #     with socket.create_connection(("localhost", 4221), timeout=1) as client_socket:
    #         client_socket.sendall(b"GET /echo/abc HTTP/1.1\r\n\r\n")
    #         response = client_socket.recv(1024).decode()
    #         self.assertIn("HTTP/1.1 200 OK", response)
    #         self.assertIn("Content-Type: text/plain", response)
    #         self.assertIn("Content-Length: 3", response)
    #         self.assertIn("\r\n\r\nabc", response)


if __name__ == "__main__":
    unittest.main()     