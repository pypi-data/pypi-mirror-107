from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import urllib.parse
from urllib.parse import parse_qs
import typing
import json
import io, os

__version__ = "1.0.5"

def render_template(file):
    if file != None:
        with open("templates/" + file, "r") as f:
            data = f.read()
        return {"html": data, "content-type": "text/html"} 

def PlainResponse(data : str):
#    data = data.replace("\n", "<br>")
    data = f"<!DOCTYPE html><html><body><h2>{data}</h2></body></html>"
    return {"html": data, "content-type": "text/html"} 

def HTMLResponse(data : str):
    return {"html": data, "content-type": "text/html"} 

def JsonResponse(data : dict):
    return {"json": json.dumps(data), "content-type": "application/json"}  
    
def ImageResponse(image_object_or_file_name, mimetype="image/png"):
    if isinstance(image_object_or_file_name, io.BytesIO):
        return {"image": image_object_or_file_name, "content-type": mimetype}
    else:
        with open(image_object_or_file_name, "rb") as f:
            obj = io.BytesIO(f.read())
        return {"image": obj, "content-type": mimetype}

class Request:
    def __init__(self, args=None,headers=None,data=None,json=None,method=None):
        self.args = args  
        self.headers = headers
        self.data = data
        self.json = json    
        self.method = method        

class MakeAPIRequest(BaseHTTPRequestHandler):       
                            
    def do_POST(self):
        for route, fn, meth in self.routes:
            if meth != "POST":
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()  
                my_html = """<!DOCTYPE html>
                <html>
                <body>
                <h1>Internal Server Error</h1>
                <p>This HTTP Request does not support GET requests.</p>
                </body>
                </html>
                """             
                return self.wfile.write(bytes(my_html, "utf-8"))                            
            if self.path == route:
                self.send_response(200)
                headers = self.headers
                content_length = int(headers['Content-Length'])  
                data = self.rfile.read(content_length)
                data = data.decode("utf-8")                
                json = data
                request = Request(headers=headers, data=data, json=json, method=meth)
                func = fn(request=request)
                self.send_header("Content-type", func["content-type"])
                self.end_headers()  
                try:
                    func["json"]  
                except KeyError:
                    try:
                        func["image"]
                    except KeyError:
                        self.wfile.write(bytes(func["html"],"utf-8"))
                    else:
                        my_func_io = func["image"]          
                                       
                        self.wfile.write(my_func_io.read())
                else:
                    self.wfile.write(bytes(func["json"],"utf-8"))  
                    
    def do_GET(self):
        for route, fn, meth in self.routes:
            if meth != "GET":
                my_html = """<!DOCTYPE html>
                <html>
                <body>
                <h1>Internal Server Error</h1>
                <p>This HTTP Request does not support GET requests.</p>
                </body>
                </html>
                """             
                return self.wfile.write(bytes(my_html, "utf-8"))       
            if "?" in self.path:
                r = [route]
                p_list = self.path.split("?")
                args = parse_qs(urllib.parse.urlparse(self.path).query)
                func = fn(request=Request(args=args, headers=self.headers, method=meth))                
            else:                
                p_list = [self.path] 
                func = fn(request=Request(args=None, method=meth))                
                r = [route]        
            if p_list[0] == r[0]:                                 
                self.send_response(200)
                self.send_header("Content-type", func["content-type"])
                self.end_headers()
                try:
                    func["json"]
                except KeyError:
                    try:
                        func["image"]
                    except KeyError:
                        self.wfile.write(bytes(func["html"],"utf-8"))
                    else:
                        my_func_io = func["image"]          
                                       
                        self.wfile.write(my_func_io.read())                        
                else:
                    self.wfile.write(bytes(func["json"], "utf-8"))

class MakeAPI():
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.handler = MakeAPIRequest
        self.handler.routes = []
        
    def post(self, route):
        def decorator(f : typing.Callable, *args, **kwargs) -> typing.Callable:
            self.handler.routes.append((route, f, "POST")) 
        return decorator                                                                                                                         
    def get(self,route):
        
        def decorator(f : typing.Callable, *args, **kwargs) -> typing.Callable:              
            self.handler.routes.append((route, f, "GET"))
        return decorator
                                                   
    def run(self):
        server_address = (self.server_address, self.server_port)
        httpd = HTTPServer(server_address, self.handler)
        print("* Running on http://{}:{}/ (CTRL+C to quit)".format(self.server_address, self.server_port))
        print("* Endpoints:")
        for route, func, meth in self.handler.routes:
            print(f"    * {route} [{meth}]")
        httpd.serve_forever()                                                                                                                                                                                                  