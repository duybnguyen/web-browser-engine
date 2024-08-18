from URL import URL
from utils.defs import ENTITIES
# prints the body of the response skipping over html tags
def show(body):
   in_tag = False
   for c in body:
      if c == "<":
         in_tag = True
      if c == ">":
         in_tag = False
      elif not in_tag:
         if c in ENTITIES:
            c = ENTITIES[c]
         print(c, end="")

def load(url):
   body = url.request()
   show(body)


if __name__ == "__main__":
   import sys
   load(URL(sys.argv[1]))
