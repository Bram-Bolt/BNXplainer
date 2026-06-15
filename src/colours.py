import matplotlib.colors as mcolors

#defining colours
beige = "#ece4dc"
olive = "#7D8F05"
olive_light = "#CCD77F"
grey  = "#626262"
black = "black"
white = "white"
maroon = "#5B0917"
light_grey = "#EBE9E6"
beige_dark = "#ddd5cb"  
beige_mid  = "#e8e0d8"   
shadow = "#7a6560"   
blue = "#384A75"   
terracotta = "#7a3830"   
dusty_rose = "#ae9a92" 
mauve = "#795554" 
sage = "#adb886"   
shadow_dark = "#4a3830" 
shadow_darkest = "#3a2820"
card_bg = "#faf7f4" 

button_bg  = "#c8bfb5"

border_light = "#f5f0eb"  
border_dark  = mauve     

# diagram node colours
regular_node = "#C8C0B5" 
target_node  = "#A1737B" 
evidence_node = "#7E889D"  

#private colour table used by make_node_cmap for diagrams
_diagram_colours = {
    "beige": beige,
    "olive": olive,
    "grey":  grey,
    "black": black,
    "white": white,
    "maroon": maroon,
    "olive_light": olive_light,
    "light_grey": light_grey,
    "regular_node": regular_node,
    "target_node": target_node,
    "evidence_node": evidence_node

}

def make_node_cmap(name: str) -> mcolors.LinearSegmentedColormap:
    hex_color = _diagram_colours[name]
    #same colour twice= flat gradient, so pyagrum always gets exactly the colour
    return mcolors.LinearSegmentedColormap.from_list(name, [hex_color, hex_color])