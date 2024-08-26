from utils.defs import CANVAS_HSTEP, CANVAS_VSTEP, CANVAS_WIDTH, Text
from utils.helpers import get_font

class Layout:
   def __init__(self, tokens):
      self.tokens = tokens
      self.display_list = []

      self.cursor_x = CANVAS_HSTEP
      self.cursor_y = CANVAS_VSTEP
      self.weight = "normal"
      self.style = "roman"
      self.font_size = 16

      self.line = []
      for tok in tokens:
         self.token(tok)
      self.flush()

   def token(self, tok):
      if isinstance(tok, Text):
         for word in tok.text.split():
               self.word(word)
      # examine tag tokens to change font when directed by the page
      elif tok.tag == "i":
         self.style = "italic"
      elif tok.tag == "/i":
         self.style = "roman"
      elif tok.tag == "b":
         self.weight = "bold"
      elif tok.tag == "/b":
         self.weight = "normal"
      elif tok.tag == "small":
         self.font_size -= 2
      elif tok.tag == "/small":
         self.font_size += 2
      elif tok.tag == "big":
         self.font_size += 4
      elif tok.tag == "/big":
         self.font_size -= 4
      elif tok.tag == "br":
         self.flush()
      elif tok.tag == "/p":
         self.flush()
         self.cursor_y += CANVAS_VSTEP

   def flush(self):
      if not self.line: return
      # align the words using the ascent of the tallest character on that line
      metrics = [font.metrics() for _, _, font in self.line]

      max_ascent = max([metric["ascent"] for metric in metrics])
      baseline = self.cursor_y + 1.25 * max_ascent

      # add the new y position for that word along with the other arguments to display list
      for x, word, font in self.line:
         y = baseline - font.metrics("ascent")
         self.display_list.append((x, y, word, font))

      # update x and y pointers to point at the next line
      max_descent = max([metric["descent"] for metric in metrics])
      self.cursor_y = baseline + 1.25 * max_descent
      self.cursor_x = CANVAS_HSTEP
      self.line = []



   
   def word(self, word):
      font = get_font(self.font_size, self.weight, self.style)
      # horizontal space in pixels
      word_width = font.measure(word)
      space_width = font.measure(" ")
         
      # flush line once the words in self.line fill up the line
      if self.cursor_x + word_width >= CANVAS_WIDTH - CANVAS_HSTEP:
         self.flush()
      self.line.append((self.cursor_x, word, font))
      self.cursor_x += word_width + space_width