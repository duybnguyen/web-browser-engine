import tkinter

from utils.defs import CANVAS_WIDTH, CANVAS_HEIGHT, SCROLL_STEP, CANVAS_VSTEP
from app.URL import URL
from app.HTMLParser import HTMLParser
from app.Layout import Layout
from utils.helpers import print_tree

class Browser: 
   def __init__(self):
      # creates a window and positions a canvas inside that window
      self.window = tkinter.Tk()
      self.canvas = tkinter.Canvas(
         self.window,
         width = CANVAS_WIDTH,
         height = CANVAS_HEIGHT
      )
      self.canvas.pack(fill = tkinter.BOTH, expand = True)
      self.display_list = []
      self.scroll = 0
      self.last_width = CANVAS_WIDTH
      
      self.window.bind("<Configure>", self.on_resize)
      self.window.bind("<MouseWheel>", self.scroll_down)
      self.window.bind("<KeyPress-Down>", self.scroll_down)
      self.window.bind("<KeyPress-Up>", self.scroll_up)

      self.nodes = None

   def draw(self):
      self.canvas.delete("all")
      for x, y, word, font in self.display_list:
         # skip drawing characters that are offscreen
         if y > self.scroll + CANVAS_HEIGHT: continue
         if y + CANVAS_VSTEP < self.scroll: continue

         #  simulate scrolling by moving the content up and down based on scroll value
         self.canvas.create_text(x, y - self.scroll, text=word, font=font, anchor='nw')

   # write body to canvas
   def load(self, url):
      if url.lower() == "about:blank":
         self.display_list = []  # Render an empty page
         self.draw()
         return

      try:
         body = URL(url).request()
         self.nodes = HTMLParser(body).parse()
         self.display_list = Layout(self.nodes).display_list
         self.draw()
      except Exception as e:
         # If any error occurs, load about:blank
         print(f"Error loading URL: {e}")
         self.display_list = []  # Ensure the display list is cleared
         self.load("about:blank")

   def on_resize(self, e):
      # Only recalculate layout if the width changes
      if e.width != self.last_width:
         self.last_width = e.width

   def scroll_down(self, e):
      self.scroll += SCROLL_STEP
      self.draw()

   def scroll_up(self, e):
      self.scroll = max(0, self.scroll - SCROLL_STEP)
      self.draw()
   
