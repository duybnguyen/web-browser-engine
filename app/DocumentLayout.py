from app.BlockLayout import BlockLayout
from utils.defs import CANVAS_HSTEP, CANVAS_VSTEP, CANVAS_WIDTH

class DocumentLayout:
   def __init__(self, node):
      self.node = node
      self.parent = None
      self.children = []

   def layout(self):
      child = BlockLayout(self.node, self, None)
      self.children.append(child)

      self.width = CANVAS_WIDTH - 2*CANVAS_HSTEP
      self.x = CANVAS_HSTEP
      self.y = CANVAS_VSTEP
      child.layout()
      self.height = child.height

   def paint(self):
      return []