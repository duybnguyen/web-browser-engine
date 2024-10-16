from utils.defs import CANVAS_HSTEP, CANVAS_VSTEP, CANVAS_WIDTH, BLOCK_ELEMENTS
from app.Element import Element
from utils.helpers import get_font
from app.Text import Text

class BlockLayout:
   def __init__(self, document_node, parent, previous):
      self.node = document_node
      self.parent = parent
      self.previous = previous
      self.children = []
      self.x = None
      self.y = None
      self.width = None
      self.height = None
      self.display_list = []


   def open_tag(self, tag):
      if tag == "i":
         self.style = "italic"
      elif tag == "b":
         self.weight = "bold"
      elif tag == "small":
         self.font_size -= 2
      elif tag == "big":
         self.font_size += 4
      elif tag == "br":
         self.flush() # new line


   def close_tag(self, tag):
      if tag == "i":
         self.style = "roman"
      elif tag == "b":
         self.weight = "normal"
      elif tag == "small":
         self.font_size += 2
      elif tag == "big":
         self.font_size -= 4
      elif tag == "p":
         self.flush() # new line
         self.cursor_y += CANVAS_VSTEP


   def recurse(self, tree):
      if isinstance(tree, Text):
         for word in tree.text.split():
            self.word(word)

      else:
         self.open_tag(tree.tag)
         for child in tree.children:
            self.recurse(child)
         self.close_tag(tree.tag)


   def layout_intermediate(self):
      previous = None
      for child in self.node.children:
         next = BlockLayout(child, self, previous)
         self.children.append(next)
         previous = next


   def layout_mode(self):
      if isinstance(self.node, Text):
         return "inline"
      elif any([isinstance(child, Element) and \
               child.tag in BLOCK_ELEMENTS
               for child in self.node.children]):
         return "block"
      elif self.node.children:
         return "inline"
      else:
         return "block"
      

   def layout(self):
      self.x = self.parent.x
      self.width = self.parent.width

      if self.previous:
         self.y = self.previous.y + self.previous.height
      else:
         self.y = self.parent.y

      mode = self.layout_mode()
      if mode == "block":
         previous = None
         for child in self.node.children:
               next = BlockLayout(child, self, previous)
               self.children.append(next)
               previous = next
      else:
         self.cursor_x = 0
         self.cursor_y = 0
         self.weight = "normal"
         self.style = "roman"
         self.font_size = 12

         self.line = []
         self.recurse(self.node)
         self.flush()

      for child in self.children:
         child.layout()

      if mode == "block":
         self.height = sum([
            child.height for child in self.children])
      else:
         self.height = self.cursor_y


   def flush(self):
      if not self.line: return

      # align the words using the ascent of the tallest character on that line
      metrics = [font.metrics() for _, _, font in self.line]

      max_ascent = max([metric["ascent"] for metric in metrics])
      baseline = self.cursor_y + 1.25 * max_ascent

      # add the new y position for that word along with the other arguments to display list
      for rel_x, word, font in self.line:
         x = self.x + rel_x
         y = self.y + baseline - font.metrics("ascent")
         self.display_list.append((x, y, word, font))

      # update x and y pointers to point at the next line
      max_descent = max([metric["descent"] for metric in metrics])
      self.cursor_y = baseline + 1.25 * max_descent
      self.cursor_x = 0
      self.line = []


   # applies the current font size, weight and style to the passed on word and saves that words x postion in a line array and calculates the x position for the next word
   def word(self, word):
      font = get_font(self.font_size, self.weight, self.style)
      # horizontal space in pixels
      word_width = font.measure(word)
      space_width = font.measure(" ")
         
      # flush line once the line fill up the line
      if self.cursor_x + word_width > self.width:
         self.flush()
      self.line.append((self.cursor_x, word, font))
      self.cursor_x += word_width + space_width


   def paint(self):
      return self.display_list