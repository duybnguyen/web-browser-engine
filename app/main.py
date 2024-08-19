import tkinter
import sys

from app.Browser import Browser

if __name__ == "__main__":
   browser = Browser()
   browser.load(sys.argv[1])
   tkinter.mainloop()
   
