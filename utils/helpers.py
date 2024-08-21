import tkinter.font
import re
from utils.defs import ENTITIES
from utils.defs import CANVAS_WIDTH, CANVAS_HSTEP, CANVAS_VSTEP

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

# add each character and its position to a list
def layout(text):
   display_list = []
   cursor_x, cursor_y = CANVAS_HSTEP, CANVAS_VSTEP
   font = tkinter.font.Font()
   for word in text.split(): 
      w = font.measure(word)
      if word == "\r\n" or word == "\n":
         cursor_y += CANVAS_VSTEP   # Move down to the next line
         cursor_x = CANVAS_HSTEP    # Reset cursor_x to the beginning of the line
         continue  # Skip adding the newline character to the display_list
         
      # keeps the text insde the canvas and add new lines when appropriate
      if cursor_x + w >= CANVAS_WIDTH - CANVAS_HSTEP:
         cursor_y += font.metrics("linespace") * 1.25
         cursor_x = CANVAS_HSTEP

      display_list.append((cursor_x, cursor_y, word))
      cursor_x += w + font.measure(" ")
   return display_list