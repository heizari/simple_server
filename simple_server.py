import os
import socket
from datetime import datetime, date
import pdb
import logging
import urllib.parse
from pprint import pformat
import ast
from route import Get, Post

class SimpleServer:
    def __init__(self) -> None:
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.VIEW_DIR = os.path.join(self.ROOT_DIR, 'view')
        self.ERROR_DIR = os.path.join(self.VIEW_DIR, 'error')
        self.changeDateSuffix()

    def changeDateSuffix(self):
        self.today = date.today().isoformat().replace('-','')
        request_file = f"request/request_{self.today}"
        self.REQUEST_OUTPUT = os.path.join(self.ROOT_DIR, request_file)
        log_file = f"log/log_{self.today}"
        self.LOG_OUTPUT = os.path.join(self.ROOT_DIR, log_file)
        logging.basicConfig(filename=self.LOG_OUTPUT, level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
        self.logger=logging.getLogger(__name__)


    def serve(self):
        print('boot server')

        try:
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            server_socket.bind(('localhost', 8880))
            server_socket.listen(10)

            while True:
                if self.today != date.today().isoformat().replace('-',''):
                    print('change date')
                    self.changeDateSuffix()
                (client_socket, address) = server_socket.accept()

                try:
                    request = client_socket.recv(4096)

                    with open(self.REQUEST_OUTPUT, 'ab') as f:
                        f.write(request)

                    response = self.createResponse(request)

                    client_socket.send(response)

                except Exception as req_error:
                    print(f'something error has occurred. check log {self.LOG_OUTPUT}')
                    self.logger.error(req_error)

                finally:
                    client_socket.close()

        finally:
            print('stop server')

    def createResponse(self, request):
        with open(self.REQUEST_OUTPUT, 'ab') as f:
            f.write(request)

        # pdb.set_trace()
        req_line, req_header, req_body, method, view_file = self.parseRequest(request)

        try:
            response_body = self.getResponseBody(view_file, method, req_body)
            response_line = "HTTP/1.1 200 OK\r\n"
        except OSError:
            response_body = self.showError('404')
            response_line = "HTTP/1.1 404 Not Found\r\n"
        response_header = self.getResponseHeader(len(response_body))

        response = (f"{response_line}{response_header}\r\n").encode() + response_body

        return response

    def getResponseBody(self, path, method, params=''):
        if method == "GET":
            # get_params = ''
            # if '?' in path:
            #     path, get_params = path.split('?')
            # print(path)
            # with open(path, "rb") as f:
            #     response_body = f.read()
            response_body = Get(path)

        elif method == "POST":
            response_body = Post(path, params.decode())

        elif method == "ERROR":
            with open(path, "rb") as f:
                response_body = f.read()


        return response_body

    def getResponseHeader(self, body_len):
        response_header = ""
        response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response_header += "Host: SimpleServer/0.1\r\n"
        response_header += f"Content-Length: {body_len}\r\n"
        response_header += "Connection: Close\r\n"
        response_header += "Content-Type: text/html\r\n"

        return response_header


    def showError(self, error_type):
        path = os.path.join(self.ERROR_DIR, f"{error_type}.html")
        return self.getResponseBody(path, "ERROR")

    def parseRequest(self, request):
        req_line, remain = request.split(b"\r\n", maxsplit=1)
        req_header, req_body = remain.split(b"\r\n\r\n", maxsplit=1)
        method, abs_path, http_ver = req_line.decode().split()
        view_file = abs_path.lstrip('/') if abs_path != '/' else 'index'

        return req_line, req_header, req_body, method, view_file

if __name__ == "__main__":
    server = SimpleServer()
    server.serve()
