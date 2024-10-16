import tkinter

from utils.defs import CANVAS_WIDTH, CANVAS_HEIGHT, SCROLL_STEP, CANVAS_VSTEP
from app.URL import URL
from app.HTMLParser import HTMLParser
from utils.helpers import paint_tree
from app.DocumentLayout import DocumentLayout


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

   # from a populated display_list, draws the words based on their x and y positions and font
   def draw(self):
      self.canvas.delete("all")
      for x, y, word, font in self.display_list:
         # skip drawing characters that are offscreen
         if y > self.scroll + CANVAS_HEIGHT: continue
         if y + CANVAS_VSTEP < self.scroll: continue

         #  simulate scrolling by moving the content up and down based on scroll value
         self.canvas.create_text(x, y - self.scroll, text=word, font=font, anchor='nw')

   # populates display list with the positions of each word and then calls draw on those words
   def load(self, url):
      if url.lower() == "about:blank":
         self.display_list = []  # Render an empty page
         self.draw()
         return

      try:
         body = URL(url).request()
         self.document_node = HTMLParser(body).parse()
         self.document = DocumentLayout(self.document_node)
         self.document.layout()
         self.display_list = []
         paint_tree(self.document, self.display_list)
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

   # redraws characters once user scrolls
   def scroll_down(self, e):
      self.scroll += SCROLL_STEP
      self.draw()

   def scroll_up(self, e):
      self.scroll = max(0, self.scroll - SCROLL_STEP)
      self.draw()
   
