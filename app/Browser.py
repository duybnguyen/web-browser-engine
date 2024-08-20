import tkinter
from utils.defs import CANVAS_WIDTH, CANVAS_HEIGHT, SCROLL_STEP, CANVAS_VSTEP
from app.URL import URL
from utils.helpers import lex, layout

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
      self.content_body = ""
      self.last_width = CANVAS_WIDTH
      
      self.window.bind("<Configure>", self.on_resize)
      self.window.bind("<MouseWheel>", self.scroll_down)
      self.window.bind("<KeyPress-Down>", self.scroll_down)
      self.window.bind("<KeyPress-Up>", self.scroll_up)

   def draw(self):
      self.canvas.delete("all")
      for x, y, c in self.display_list:
         # skip drawing characters that are offscreen
         if y > self.scroll + CANVAS_HEIGHT: continue
         if y + CANVAS_VSTEP < self.scroll: continue

         self.canvas.create_text(x, y - self.scroll, text = c)

   # write body to canvas
   def load(self, url):
      parsedURL = URL(url)
      parsedURL = parsedURL.request()
      self.content_body = lex(parsedURL)
      self.display_list = layout(self.content_body)
      self.draw()

   def on_resize(self, e):
      # Only recalculate layout if the width changes
      if e.width != self.last_width:
         self.last_width = e.width
         self.display_list = layout(self.content_body)
         self.draw()

   def scroll_down(self, e):
      self.scroll += SCROLL_STEP
      self.draw()

   def scroll_up(self, e):
      self.scroll -= SCROLL_STEP
      self.draw()
   
