# main.py
import importlib
import os
import pkgutil
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
import inspect

from settings import DEBUG


# This decorator will be used to mark view functions that should be hyphen cased for URLs
def use_hyphen_case(func):
    func.use_hyphen_case = True
    return func


class WebFramework(BaseHTTPRequestHandler):
    # Define routes as a class variable so it's shared among all instances
    routes = {}

    def do_GET(self):
        parsed_path = urlparse(self.path).path.strip('/')
        if parsed_path in self.routes:
            handler = self.routes[parsed_path]
            response_body = json.dumps(handler())
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response_body.encode())
        else:
            self.send_error(404, 'Not Found')


def load_routes():
    # Import all modules in the views package and load all their functions into WebFramework.routes
    for _, module_name, _ in pkgutil.iter_modules(['views']):
        module = importlib.import_module(f'views.{module_name}')
        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            # Check if attr is a function defined in this module (not imported)
            if callable(attr) and attr.__module__ == module.__name__:
                route = attr.__name__
                if hasattr(attr, 'use_hyphen_case') and getattr(attr, 'use_hyphen_case', False):
                    route = route.replace('_', '-')
                WebFramework.routes[route] = attr


if __name__ == '__main__':
    load_routes()
    server = HTTPServer(('localhost', 8080), WebFramework)
    if DEBUG:
        print('Starting server at http://localhost:8080')
        print('Available routes:')
        for route in WebFramework.routes:
            print(f' - /{route}')
    server.serve_forever()
