#!/usr/bin/python
import json
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from postgres_client import *

PORT_NUMBER = 5556
ROUTE = "route"
DATA = "data"

ROUTE_AGENT_TRACKING = "agent_tracking"
ROUTE_CONTROLLER_TRACKING = "controller_tracking"
DATABASE_HOST = "database_host"

CONNECTION_FILE = "/root/sqlite/db/pythonsqlite.db"


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        print('test print')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("I'm ready !")
        return

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        json_data = self.rfile.read(content_len)
        print json_data

        try:
            data = json.loads(json_data)
            route = data[ROUTE]
            data_json = {}
            if DATA in data:
                data_json = data[DATA]
            handle_route(self, route, data_json)
        except ValueError:
            print('Got invalid json format, ignoring request')
            print json_data
            self.send_response(200, 'Error: invalid json format')
            self.send_header('content-type', 'application/json')
            self.end_headers()


def handle_route(handler, route, data_array):
    if route == ROUTE_AGENT_TRACKING :
        print route
        try:
            insert_data(data_array)

            handler.send_response(200)
            handler.send_header('content-type', 'application/json')
            handler.end_headers()
        except TypeError as e:
            print('Got invalid JSON format: ' + e.message)
            handler.send_response(400, 'Error: invalid json format')
            handler.send_header('content-type', 'application/json')
            handler.end_headers()
    elif route == ROUTE_CONTROLLER_TRACKING:
        print route
        #TODO to implement

try:
    # Create a web server and define the handler to manage the
    # incoming request
    def create_connection(CONNECTION_FILE):
        is_connected = False
        # host = current_config.get(DATABASE_HOST, "localhost")
        while not is_connected:
            is_connected = open_connection("http://127.0.0.1:5556/")
            time.sleep(5)


    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()