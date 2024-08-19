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
   for c in text: 
      display_list.append((cursor_x, cursor_y, c))
      cursor_x += CANVAS_HSTEP
      # keeps the text insde the canvas and add new lines when appropriate
      if cursor_x >= CANVAS_WIDTH - CANVAS_HSTEP:
         cursor_y += CANVAS_VSTEP
         cursor_x = CANVAS_HSTEP
   return display_list