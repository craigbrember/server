# useful reference material:
#http://joaoventura.net/blog/2017/python-webserver/
#https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python/51559006#51559006
#https://wiki.python.org/moin/BaseHttpServer
#https://pymotw.com/2/BaseHTTPServer/  this is an excellent article
#
# useful reference if we need to kill a process where server hasn't shut down properly
#https://stackoverflow.com/questions/17780291/python-socket-error-errno-98-address-already-in-use
# lsof -i:8000
# sudo kill -9 <process id>
#
# http://localhost:8000/?firstname=john&surname=smith provides index page with query involving firstname
# and surname
#
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import urllib.parse

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000

class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        print('in do_HEAD')
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    
    def do_GET(self):
        # entering here when self.command = 'GET'
        parsed_path = urllib.parse.urlparse(self.path)
        '''
        message_parts = [
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                'HEADERS RECEIVED:',
                ]
        '''
        if parsed_path.path == '/' or parsed_path.path == '' or parsed_path.path == '/index.html':
           self.send_response(200)
           self.end_headers()
           print('query = ' + str(parsed_path.query)) 
           fin = open('index.html')
           content = fin.read()
           fin.close()
           self.wfile.write(content.encode())
           return
        if parsed_path.path == '/temp.html':
           self.send_response(200)
           self.end_headers()
           query = parsed_path.query
           print('query = ' + query)
           fin = open('temp.html')
           content = fin.read()
           fin.close()
           self.wfile.write(content.encode())
           return
        if parsed_path.path == '/ipsum.html':
           self.send_response(200)
           self.end_headers()
           print('query = ' + str(parsed_path.query))
           fin = open('ipsum.html')
           content = fin.read()
           fin.close()
           self.wfile.write(content.encode())
           return
        self.send_response(404)
        self.end_headers()
        content = 'Oops...page not found'
        self.wfile.write(content.encode())
        return

    def do_POST(self):
        # TODO: untested!!
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write('\tUploaded %s as "%s" (%d bytes)\n' % \
                        (field, field_item.filename, file_len))
            else:
                # Regular form value
                self.wfile.write('\t%s=%s\n' % (field, form[field].value))
        return
             
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def run():
    server = ThreadingSimpleServer((HOST_NAME, PORT_NUMBER), Handler)
    server.serve_forever()


if __name__ == '__main__':
    run()