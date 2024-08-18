import socket

class URL:
   def __init__(self, url):
      if "/" not in url:
         url = url + "/"
      self.host, url = url.split("/", 1) 
      self.path = "/" + url


      def request(self):
         # create a socket
         s = socket.socket(
            family = socket.AF_INET,
            type = socket.SOCK_STREAM,
            proto = socket.IPPROTO_TCP
         )

         # connect to the host using the socket on port 80
         s.connect((self.host, 80))

         # form a request
         request = "GET {} HTTP/1.0\r\n".format(self.path)
         request += "Host: {}\r\n".format(self.host)
         request += "\r\n" #signals end of request
         s.send(request.encode("utf8"))

         # reading the server's response
         response = s.makefile("r", encoding="utf", newline="\r\n")
         # reading the status line
         statusline = response.readline()
         version, status, explanation = statusline.split(" ", 2)
         # reading the headers
         response_headers = {}
         while True:
            line = response.readline()
            if line == "\n\r": break # if the line is just an empty line that means it's the end of the response
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
         
         # can't process these headers yet
         assert "transfer-encoding" not in response_headers
         assert "content-encoding" not in response_headers

         # read the rest of the response which is the body
         content = response.read()
         s.close()
         return content


      