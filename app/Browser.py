import tkinter
from utils.defs import CANVAS_WIDTH, CANVAS_HEIGHT, SCROLL_STEP, layout
from app.URL import URL
from utils.helpers import lex

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
      self.scroll = 0
      
      self.window.bind("<Down>", self.scrolldown)

   def draw(self):
      self.canvas.delete("all")
      for x, y, c in self.display_list:
         self.canvas_create_text(x, y - self.scroll , text = c)

   # write body to canvas
   def load(self, url):
      parsedURL = URL(url).request()
      body = lex(parsedURL)
      self.display_list = layout(body)
      self.draw()

   def scrollDown(self, e):
      self.scroll += SCROLL_STEP
      self.draw()
   
