import tkinter.font
from utils.defs import FONTS


# cache fonts in memory using a FONTS dictionary to avoid recreating the same font multiple times
def get_font(size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight, slant=style)
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]

# prints the structure of the tree for debugging
def print_tree(node, indent=0):
   print(" " * indent, node)
   for child in node.children:
      print_tree(child, indent + 2)


def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)