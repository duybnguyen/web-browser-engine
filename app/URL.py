import socket
import ssl

class URL:
   # example url: http://example.org:8080/index.html
   def __init__(self, url):
      self.scheme, url = url.split("://", 1)
      assert self.scheme in ["http", "https"]
      if self.scheme == "http":
         self.port = 80
      elif self.scheme == "https":
         self.port = 443

      if "/" not in url: # adds / only if url doesn't contain a path and the host is missing a /
         url += "/"
      self.host, url = url.split("/", 1) 

      # check if url specifies a port
      if ":" in self.host:
         self.host, port = self.host.split(":", 1)
         self.port = int(port)
      
      self.path = "/" + url


   def request(self):
      # create a socket
      s = socket.socket(
         family = socket.AF_INET,
         type = socket.SOCK_STREAM,
         proto = socket.IPPROTO_TCP
      )

      # connect to the host using the socket on self.port
      s.connect((self.host, self.port))
      # setup encryped connection if scheme is https
      if self.scheme == "https":
         ctx = ssl.create_default_context()
         s = ctx.wrap_socket(s, server_hostname = self.host)

      # form a request
      request = "GET {} HTTP/1.0\r\n".format(self.path)
      request += "Host: {}\r\n".format(self.host)
      request += "\r\n" #signals end of request
      s.send(request.encode("utf-8"))

      # reading the server's response
      response = s.makefile("r", encoding="utf-8", newline="\r\n")
      # reading the status line
      statusline = response.readline()
      version, status, explanation = statusline.split(" ", 2)
      # reading the headers
      response_headers = {}
      while True:
         line = response.readline() # after every call readline's internal pointer points to the next line
         if line == "\r\n": break # if the line is just an empty line that means it's the end of the response
         header, value = line.split(":", 1)
         response_headers[header.casefold()] = value.strip() # save headers
      
      # can't process these headers yet
      assert "transfer-encoding" not in response_headers
      assert "content-encoding" not in response_headers

      # read the rest of the response which is the body
      content = response.read()
      s.close()
      return content
