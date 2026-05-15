import matplotlib.colors as mcolors

#defining colours
beige = "#ece4dc"
olive = "#7D8F05"
grey  = "#626262"
black = "black"
white = "white"
maroon = "#5B0917"

#private colour table used by make_node_cmap for diagrams
_diagram_colours = {
    "beige": beige,
    "olive": olive,
    "grey":  grey,
    "black": black,
    "white": white,
    "maroon": maroon
}

def make_node_cmap(name: str) -> mcolors.LinearSegmentedColormap:
    hex_color = _diagram_colours[name]
    #same colour twice= flat gradient, so pyagrum always gets exactly the colour
    return mcolors.LinearSegmentedColormap.from_list(name, [hex_color, hex_color])