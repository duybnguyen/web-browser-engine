from utils.defs import Text, Element

class HTMLParser:
   def __init__(self, body):
      self.body = body
      self.unfinished = []

   def add_text(self, text):
      parent = self.unfinished[-1]
      node = Text(text, parent)
      parent.children.append(node)

   def add_tag(self, tag):
      if tag.startswith("/"):
         node = self.unfinished.pop()
         parent = self.unfinished[-1]
         parent.children.append(node)
      else:
         parent = self.unfinished[-1]
         node = Element(tag, parent)
         self.unfinished.append(node)

   def parse(self):
      text = ""
      in_tag = False
      for c in self.body:
         if c == "<":
            in_tag = True
            if text: self.add_text(text) # only append if there's text in buffer
            text = ""
         elif c == ">":
            in_tag = False
            self.add_tag(text) # append regardless if there's content inside the tags
            text = ""
         else:
            text += c
      # dumps any accumulated buffered text to the tree
      if not in_tag and text:
         self.add_text(text)
      return self.finish()
