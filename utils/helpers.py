import tkinter.font
from utils.defs import CANVAS_WIDTH, CANVAS_HSTEP, CANVAS_VSTEP
from app.Text import Text
from app.Tag import Tag

# returns the body of the response instantiating it with the appropriate class
def lex(body):
   out = []
   buffer = ""
   in_tag = False
   for c in body:
      if c == "<":
         in_tag = True
         if buffer: out.append(Text(buffer))
         buffer = ""
      if c == ">":
         in_tag = False
         out.append(Tag(buffer))
         buffer = ""
      else:
         buffer += c
   if not in_tag and buffer:
      out.append(Text(buffer))
   return out

# add each character and its position to a list
def layout(tokens):
   display_list = []
   cursor_x, cursor_y = CANVAS_HSTEP, CANVAS_VSTEP
   font = tkinter.font.Font()
   for token in tokens: 
      if isinstance(token, Text):
         for word in token.text.split():
            font = tkinter.font.Font(
               size = 16,
               weight = weight,
               slant = style,
            )
            w = font.measure(word) # horizontal space of a word in pixels
            if word == "\r\n" or word == "\n":
               cursor_y += CANVAS_VSTEP   # Move down to the next line
               cursor_x = CANVAS_HSTEP    # Reset cursor_x to the beginning of the line
               continue  # Skip adding the newline character to the display_list
               
            # keeps the text insde the canvas and add new lines when appropriate
            if cursor_x + w >= CANVAS_WIDTH - CANVAS_HSTEP:
               cursor_y += font.metrics("linespace") * 1.25
               cursor_x = CANVAS_HSTEP

            display_list.append((cursor_x, cursor_y, word, font))
            cursor_x += w + font.measure(" ")
      elif token.tag == "i":
         style = "italic"
      elif token.tag == "/i":
         style = "roman"
      elif token.tag == "b":
         weight = "bold"
      elif token.tag == "/b":
         weight = "normal"
   return display_list