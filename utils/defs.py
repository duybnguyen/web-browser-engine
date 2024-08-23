from dataclasses import dataclass

ENTITIES = {"&lt": "<", "&gt": ">"}
CANVAS_WIDTH, CANVAS_HEIGHT = 800, 600
CANVAS_HSTEP, CANVAS_VSTEP = 12, 18 # how many pixels we seperate each character in the canvas by
SCROLL_STEP = 100
FONTS = {}

@dataclass
class Text:
    text: str

@dataclass
class Tag:
    tag: str