import tkinter
from utils.defs import CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_HSTEP, CANVAS_VSTEP

class Browser: 
   def __init__(self):
      # creates a window and positions a canvas inside that window
      self.window = tkinter.Tk()
      self.canvas = tkinter.Canvas(
         self.window,
         width = CANVAS_WIDTH,
         height = CANVAS_HEIGHT
      )
      self.canvas.pack()

   # write body to canvas
   def load(self, body):
      cursor_x, cursor_y = CANVAS_HSTEP, CANVAS_VSTEP # pointer to where the next character will go
      for c in body:
         self.canvas.create_text(cursor_x, cursor_y, text = c)
         cursor_x += CANVAS_HSTEP
         # keeps the text insde the canvas
         if cursor_x >= CANVAS_WIDTH - CANVAS_HSTEP:
            cursor_y += CANVAS_VSTEP
            cursor_x = CANVAS_HSTEP
