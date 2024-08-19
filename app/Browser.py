import tkinter
from utils.defs import CANVAS_WIDTH, CANVAS_HEIGHT

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
      HSTEP, VSTEP = 12, 18
      cursor_x, cursor_y = HSTEP, VSTEP
      for c in body:
         self.canvas.create_text(cursor_x, cursor_y, text = c)
         cursor_x += HSTEP
         # keeps the text 
         if cursor_x >= CANVAS_WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
