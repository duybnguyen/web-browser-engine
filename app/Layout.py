

from utils.defs import CANVAS_HSTEP, CANVAS_VSTEP, CANVAS_WIDTH
from utils.helpers import get_font
from app.Text import Text

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
      elif tok.tag == "i":
         self.style = "italic"
      elif tok.tag == "/i":
         self.style = "roman"
      elif tok.tag == "b":
         self.weight = "bold"
      elif tok.tag == "/b":
         self.weight = "normal"
      elif tok.tag == "small":
         self.size -= 2
      elif tok.tag == "/small":
         self.size += 2
      elif tok.tag == "big":
         self.size += 4
      elif tok.tag == "/big":
         self.size -= 4
      elif tok.tag == "br":
         self.flush()
      elif tok.tag == "/p":
         self.flush()
         self.cursor_y += CANVAS_VSTEP

   def flush(self):
      if not self.line: return

      metrics = [font.metrics() for x, word, font in self.line]

      max_ascent = max([metric["ascent"] for metric in metrics])
      baseline = self.cursor_y + 1.25 * max_ascent

      for x, word, font in self.line:
         y = baseline - font.metrics("ascent")
         self.display_list.append((x, y, word, font))

      max_descent = max([metric["descent"] for metric in metrics])

      self.cursor_y = baseline + 1.25 * max_descent
      self.cursor_x = CANVAS_HSTEP
      self.line = []



   
   def word(self, word):
      font = get_font(self.font_size, self.weight, self.style)
      # horizontal space in pixels
      word_width = font.measure(word)
      space_width = font.measure(" ")
         
      # wraps word if word width exceeds canvas width and hstep
      if self.cursor_x + word_width >= CANVAS_WIDTH - CANVAS_HSTEP:
         self.flush()
      self.line.append((self.cursor_x, word, font))
      self.cursor_x += word_width + space_width