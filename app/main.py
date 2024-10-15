import tkinter
import sys

from app.Browser import Browser

if __name__ == "__main__":
   browser = Browser()
   # loads webpage using url
   browser.load(sys.argv[1])
   
   # starts event handling cycle
   tkinter.mainloop()
   
