from utils.defs import ENTITIES

# returns the body of the response skipping over html tags
def lex(body):
   text = ""
   in_tag = False
   for c in body:
      if c == "<":
         in_tag = True
      if c == ">":
         in_tag = False
      elif not in_tag:
         if c in ENTITIES:
            c = ENTITIES[c]
         text += c
   return text