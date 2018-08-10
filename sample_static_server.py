from socket import *
import re

from multiprocessing import Process

HTML_ROOT_DIR = "./html"


class HTTPServer(object):
    """define socket,init socket,reponse,send,close socket"""
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def start(self):
        self.server_socket.listen(128)
        while True:
            client_socket, client_addr = self.server_socket.accept()
            print("Client connected,Address:%s,%s", client_addr)
            handle_client_process = Process(target=self.handle, args=(client_socket,))
            handle_client_process.start()
            client_socket.close()

    def handle(self, client_socket):
        request_data = client_socket.recv(1024)
        print("request data:", request_data)
        request_lines = request_data.splitlines()

        #analyse request
        request_start_line =  request_lines[0]
        print(request_start_line)
        file_name = re.match(r"\w+ +(/[^ ]*) ", request_start_line.decode("utf-8")).group(1)

        if file_name == "/":
            file_name = "/index.html"

        try:
            file = open(HTML_ROOT_DIR + file_name, "rb")
        except  IOError:
            response_start_line = "HTTP/1.1 404 Not Found\r\n"
            response_headers = "Server: My server\r\n"
            response_body = "The file is not found!"
        finally:
            file_data = file.read()
            file.close()

            response_start_line = "HTTP/1.1 200 OK\r\n"
            response_headers = "Server: My server\r\n"
            response_body = file_data.decode("utf-8")

        response = response_start_line + response_headers + "\r\n" + response_body
        client_socket.send(bytes(response, "utf-8"))

        client_socket.close()

    def bind(self, port):
        self.server_socket.bind(("", port))

def main():
    server  = HTTPServer()
    server.bind(8899)
    server.start()


if __name__ == "__main__":
    main()