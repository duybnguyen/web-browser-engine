import tkinter
import sys

from app.URL import URL
from app.Browser import Browser
from utils.helpers import lex

if __name__ == "__main__":
   url = URL(sys.argv[1])
   body = lex(url.request())
   browser = Browser()
   browser.load(body)
   tkinter.mainloop()
   
