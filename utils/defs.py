ENTITIES = {"&lt": "<", "&gt": ">"}
CANVAS_WIDTH, CANVAS_HEIGHT = 800, 600
CANVAS_HSTEP, CANVAS_VSTEP = 12, 18 # how many pixels we seperate each character in the canvas by
SCROLL_STEP = 100
FONTS = {}
SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]
HEAD_TAGS = [
   "base", "basefont", "bgsound", "noscript",
   "link", "meta", "title", "style", "script",
]
BLOCK_ELEMENTS = [
    "html", "body", "article", "section", "nav", "aside",
    "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "header",
    "footer", "address", "p", "hr", "pre", "blockquote",
    "ol", "ul", "menu", "li", "dl", "dt", "dd", "figure",
    "figcaption", "main", "div", "table", "form", "fieldset",
    "legend", "details", "summary"
]