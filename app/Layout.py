import tkinter

from utils.defs import CANVAS_HSTEP, CANVAS_VSTEP, CANVAS_WIDTH
from app.Text import Text

class Layout:
   def __init__(self, tokens):
      self.display_list = []
      self.cursor_x = CANVAS_HSTEP
      self.cursor_y = CANVAS_VSTEP
      self.weight = "normal"
      self.style = "roman"
      self.font_size = 16

      for tok in tokens:
         self.token(tok)

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
   
   def word(self, word):
      font = tkinter.font.Font(
         size = self.font_size,
         weight = self.weight,
         slant = self.style,
      )
      # horizontal space in pixels
      word_width = font.measure(word)
      space_width = font.measure(" ")

      if word == "\r\n" or word == "\n":
         self.cursor_y += CANVAS_VSTEP   # move down to the next line
         self.cursor_x = CANVAS_HSTEP    # reset cursor_x to the beginning of the line
         return  # skip further processing for the newline character
         
      # wraps word if word width exceeds canvas width and hstep
      if self.cursor_x + word_width >= CANVAS_WIDTH - CANVAS_HSTEP:
         self.cursor_y += font.metrics("linespace") * 1.25
         self.cursor_x = CANVAS_HSTEP

      self.display_list.append((self.cursor_x, self.cursor_y, word, font))
      self.cursor_x += word_width + space_width