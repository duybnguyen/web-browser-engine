class URL:
   def __init__(self, url):
      if "/" not in url:
         url = url + "/"
      """separate hostname from path by splitting at the first occurrence of /"""
      self.host, url = url.split("/", 1) 
      self.path = "/" + url

      