from app.Text import Text
from app.Element import Element
from utils.defs import SELF_CLOSING_TAGS, HEAD_TAGS

class HTMLParser:
   def __init__(self, body):
      self.body = body
      self.unfinished = []


   def get_attributes(self, text):
      parts = text.split()
      tag = parts[0].casefold()
      attributes = {}
      # slice the tag name from the rest of the attributes
      for attrpair in parts[1:]:
         if "=" in attrpair:
            key, value = attrpair.split("=", 1)
            if len(value) > 2 and value[0] in ["'", "\""]:
               value = value[1:-1]
            attributes[key.casefold()] = value
         else:
            attributes[attrpair.casefold()] = ""
      return tag, attributes   
   

   def implicit_tags(self, tag):
      while True:
         open_tags = [node.tag for node in self.unfinished]
         if open_tags == [] and tag != "html":
               self.add_tag("html")
         elif open_tags == ["html"] \
               and tag not in ["head", "body", "/html"]:
               if tag in HEAD_TAGS:
                  self.add_tag("head")
               else:
                  self.add_tag("body")
         elif open_tags == ["html", "head"] and \
               tag not in ["/head"] + HEAD_TAGS:
               self.add_tag("/head")
         else:
               break


   # add a text node to the tree
   def add_text(self, text):
      if text.isspace(): return # ignore text that consists only of whitespace (e.g., new lines)
      self.implicit_tags(None)

      parent = self.unfinished[-1] # access the latest tag 
      node = Text(text, parent)
      parent.children.append(node) # append the new Text node as a child of the most recent tag


   # add tag nodes to the tree
   def add_tag(self, tag):
      tag, attributes = self.get_attributes(tag)
      if tag.startswith("!"): return # ignore doctype declaration and comments
      self.implicit_tags(tag)

      # close tag finishes the last unfinished node by adding it to its parent
      if tag.startswith("/"):
         if len(self.unfinished) == 1: return # Do not close the root element prematurely
         node = self.unfinished.pop() 
         parent = self.unfinished[-1]
         parent.children.append(node)

      # # Self-closing tag: create a node and directly append it to the current parent
      elif tag in SELF_CLOSING_TAGS:
        parent = self.unfinished[-1]
        node = Element(tag, attributes, parent)
        parent.children.append(node)

      # open tag adds an unfinished node to the end of the list
      else:
         parent = self.unfinished[-1] if self.unfinished else None
         node = Element(tag, attributes, parent)
         self.unfinished.append(node) 


   # turns incomplete tree into a complete tree by finishing any unfinished nodes
   def finish(self):
      if not self.unfinished:
            self.implicit_tags(None)
      while len(self.unfinished) > 1:
         node = self.unfinished.pop()
         parent = self.unfinished[-1]
         parent.children.append(node)
      return self.unfinished.pop()


   # goes through body and adds nodes to HTML tree
   def parse(self):
      text = ""
      in_tag = False
      for c in self.body:
         if c == "<":
            in_tag = True
            if text: self.add_text(text) # only add if there's text in buffer
            text = ""
         elif c == ">":
            in_tag = False
            self.add_tag(text) # add regardless if there's content inside the tags
            text = ""
         else:
            text += c
      # dumps any accumulated buffered text as child of latest element
      if not in_tag and text:
         self.add_text(text)
      return self.finish()
