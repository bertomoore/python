'''
A set of resources for common activities related to
web design like character-escaping, color value
conversion, etc.

Some of the scripts may not be fully operational
'''

from bs4 import BeautifulSoup
from os import getcwd, mkdir
from re import match, search, findall, sub, split
from colorsys import rgb_to_hls, hls_to_rgb

this_dir = getcwd()



def load_css_file(css_src):
    in_media_query = False
    many_selectors = False
    media_query_val = ""
    current_selector = ""
    current_selector_list = []
    by_selector = {}
    by_property = {}

    def add_to_stylesheet(s,p,v):
        if not(in_media_query):
            by_selector[s][p] = v
            if p not in by_property:
                by_property[p] = {}
            if v in by_property[p]:
                by_property[p][v].append(s)
            else:
                by_property[p] = {v:[s]}
        else:
            by_selector[media_query_val][s][p] = v
            if p not in by_property[media_query_val]:
                by_property[p] = {}
            if v in by_property[media_query_val][p]:
                by_property[media_query_val][p][v].append(s)
            else:
                by_property[p] = {v:[s]}
        
    with open(css_src) as cs:
        css_lines = cs.readlines()
    
    for x in range(len(css_lines)):
        if match(r"[^@].*{",css_lines[x]):
            current_selector = search(r'([\w\.\(\)\[\]\|\$\*#>^:,~=-]*)',css_lines[x]).group()

            if "," in current_selector:
                many_selectors = True
                current_selector_list = split(r'(,[ ]?)',css_lines[x])

            elif current_selector not in by_selector:
                by_selector[current_selector] = {}

        elif ":" in css_lines[x] and '@' != css_lines[x][0]:
            prop_val_pair = split(":[ ]?",search(r'[-\w]+:[ ]?[\w\"\'\.\(\)#% /,~=-]+[ ]*[\w\"\'\.\(\)#% /,~=-]*',css_lines[x]).group())

            if many_selectors:
                for sel in current_selector_list:
                    if sel not in by_selector and not(in_media_query):
                        by_selector[sel] = {}
                    elif sel not in by_selector:
                        by_selector[media_query_val][sel] = {}
                        
                    add_to_stylesheet(sel,prop_val_pair[0],prop_val_pair[1])

                many_selectors = False

            else:
                add_to_stylesheet(current_selector,prop_val_pair[0],prop_val_pair[1])

        elif '$%' in css_lines[x]:
            in_media_query = True
            media_query_val = search(r'(max|min)',css_lines[x]).group()
            by_property[media_query_val] = {}
            by_selector[media_query_val] = {}

        elif in_media_query and match(r"^}",css_lines[x]):
            media_query_val = False

    return {"by property":by_property,"by selector":by_selector}

class CSS:
    def __init__(self,css_link):
        self.src = css_link
        self.sheet = load_css_file(css_link)

    def optimize(self,destination=None):
        if destination is None:
            destination = self.src
        ordered_by_selector = len(str(self.sheet["by selector"])) <= len(str(self.sheet["by property"]))
        return str(self.sheet["by selector"]) if ordered_by_selector else str(self.sheet["by property"])



def ext_sheet_markup(content, is_script, rel="stylesheet", page_type="text/css"):
    if isinstance(content, list):
        pass
    if is_script:
        return "<script src='{0}.js'></script>".format(content)
    else:
        return "<link href='{0}.css' rel='{1}' type='{2}' />".format(content, rel, page_type)



def new_html(title="index", dir=this_dir, stylesheets="style", scripts="index", body=False):
    page_content = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>{title}</title>
    {ext_sheet_markup(stylesheets, False)}
  </head>
  <body>
{body if body else ""}
    {ext_sheet_markup(scripts, True)}
  </body>
</html>
      """
    return page_content



def new_project(name, dir_path=this_dir):
    new_dir = f'{dir_path}/{name}'
    mkdir(new_dir)
    with open(f'{new_dir}/index.html','w') as html_file:
        html_file.write(new_html())
    with open(f'{new_dir}/index.js','w') as js_file:
        js_file.write("")
    with open(f'{new_dir}/style.css','w') as css_file:
        css_file.write("""* {
    box-sizing: border-box;
}

body {
    padding:0;
    margin:0;
}""")



def escape(string):
    unescaped = {"<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&apos;"}
    return "".join((unescaped[x] if x in unescaped else x for x in string))



def unescape(string):
    escaped = {"&lt;":"<", "&gt;":">", "&quot;":'"', "&apos;":"'"}
    return "".join((escaped[x] if x in escaped else x for x in string))



def color_blend(color_one,color_two,ratios=None):
  if ratios == None:
    ratios = [50,50]
  return "".join([hex(round(round(color_one[i*2:i*2+2],16)*ratios[0]/100+round(color_two[i*2:i*2+2],16)*ratios[1]/100))[2:] for i in range(3)])



def add_to_body(html_text, mark_up, add_to_end=True):
    if add_to_end:
        body_index = search(r'(<script[.]*>[.\n]*</script>)*<body[.]*>', html_text).start()
    else:
        body_index = search(r'<body[.]*>', html_text).end()

        return html_text[body_index:]+"\n"+mark_up+"\n"+html_text[:body_index]



def indent(num_of_spaces):
    return "".join("  " for x in range(num_of_spaces))



def get_classes(html_line, html_prep=False):
    if html_prep:
        classes = r'(?<=\.)[-\w_]+'
        return " class='{}'".format(" ".join(findall(classes, html_line))) if findall(classes, html_line)!=None else ""
    classes = r'(?<=class=("|\'))[-\w_ ]+(?=("|\'))'
    return search(classes, html_line).group().split(" ") if search(classes, html_line).group()[0]!=None else []



def get_id(html_line, html_prep=False):
    if html_prep:
        el_id = r'(?<=#)[-\w_]+'
        return "".join((" id='", search(el_id, html_line).group(), "'")) if search(el_id, html_line)!=None else ""

    el_id = r'(?<=id=("|\'))[-\w_]+(?=("|\'))'
    return search(el_id, html_line).group() if search(el_id, html_line)!=None else None
            


def update_files(dir=this_dir):
    return 0



def check_dependencies(file):
    return 0



def check_color_format(color_value):

    if search(r'(?<=#)?([0-9a-zA-Z]{6}|[0-9a-zA-Z]{3})$',color_value):
        return "hex"

    elif search(r'rgb\(\d{1,3},\d{1,3},\d{1,3}\)',color_value):
        return "rgb"

    elif search(r'hsl\(\d{1,3},(\d{1,2}|100)%?,(\d{1,2}|100)%?\)',color_value):
        return "hsl"

    else:
        return False



def new_color_format(color,new_format):
    color = color.replace(" ","")
    current_format = check_color_format(color)

    if new_format is None:
        return "Function requires two parameters: color and new format"

    elif current_format==new_format:
        return color

    elif not(current_format):
        return "Invalid color"

    if new_format=="hsl":

        rgb_vals = [(int(search(r'[0-9a-zA-Z]{6}',color).group()[2*x:2*x+2],16)/255) for x in range(3)] if current_format=="hex" else [x/255 for x in findall(r'\d+',color)]
        max_val = max(rgb_vals)
        min_val = min(rgb_vals)
        diff_val = max_val - min_val
        light = (max_val + min_val) / 2

        if diff_val==0:
            hue = 0
            saturation = 0

        else:

            if light<0.5:
                saturation = diff_val / (max_val-min_val)
            
            else:
                saturation = diff_val / (2-max_val-min_val)

            diff_r = (((max_val - rgb_vals[0]) / 6) + (diff_val / 2)) / diff_val
            diff_g = (((max_val - rgb_vals[1]) / 6) + (diff_val / 2)) / diff_val
            diff_b = (((max_val - rgb_vals[2]) / 6) + (diff_val / 2)) / diff_val 

            if rgb_vals[0]==max_val:
                hue = diff_b - diff_g

            elif rgb_vals[1]==max_val:
                hue = (1/3) + diff_r - diff_b

            elif rgb_vals[2]==max_val:
                hue = (2/3) + diff_g - diff_r

            if hue<0:
                hue += 1
            
            elif hue>1:
                hue -= 1

        return f'hsl({round(hue*360)},{round(saturation*100)},{round(light*100)})'

    elif current_format=="hsl":

        hsl_vals = [x for x in findall(r'\d+',color)]
        hue = float(hsl_vals[0]) / 360
        saturation = float(hsl_vals[1]) / 100
        light = float(hsl_vals[2]) / 100
        
        if hsl_vals[1]==0:
            return f'#{hex(round(hsl_vals[2]*255))[2:] * 3}' if new_format=="hex" else f'rgb{tuple(round(hsl_vals[2] * 255) in range(3))}'

        else:

            def hue_to_rgb(p,q,t):
                if t<0:
                    t += 1
                elif t>1:
                    t -= 1
                if t<1/6:
                    return p + (q - p) * 6 * t
                if t<1/2:
                    return q
                if t<2/3:
                    return p + (q - p) * (2/3 - t)
                return p

            q = (light * (light + saturation) if light<0.5 else light + saturation - light * saturation)
            p = 2 * light - q

            rgb_vals = [round(hue_to_rgb(p, q,hue + 1/3) * 255), round(hue_to_rgb(p, q, hue) * 255), round(hue_to_rgb(p, q,hue - 1/3) * 255)]

            return f'rgb{tuple(rgb_vals)}' if new_format=="rgb" else f'#{"".join(hex(rgb_vals[x])[2:] for x in range(3))}'


    elif new_format=="hex":
        rgb_vals = findall(r'\d+',color)
        return f'#{"".join(hex(rgb_vals[x])[2:] for x in range(3))}'


    elif new_format=="rgb":
        color = search(r'[0-9]{6}',color).group() if len(color)>=6 else search(r'[0-9]{6}').group() * 3
        return f'rgb{tuple(int(color[x*2:x*2+2],16) for x in range(3))}'



def color_scheme(base_color,scheme="complementary"):

    if base_color is None:
        return """
        color_scheme(base_color,scheme='complementary')
        complementary [hue, hue+180]
        analogous [hue-30, hue, hue+30]
        triadic [hue, hue+120, hue+240]
        quadratic [hue, hue+90, hue+180, hue+270]
        split [hue, hue+150, hue-150]
        """

    color_format = check_color_format(base_color)
    if not(color_format):
        return "Invalid base color"

    hsl_vals = findall(r'\d+',(base_color if color_format=="hsl" else new_color_format(base_color,"hsl")))


    if scheme=="complementary":
        colors = [f'hsl({(hsl_vals[0]+180*x)%360},{hsl_vals[1]}%,{hsl_vals[2]}%)' for x in range(2)]

    elif scheme=="analogous":
        colors = [f'hsl({(hsl_vals[0]+30*x)%360},{hsl_vals[1]}%,{hsl_vals[2]}%)' for x in range(-1,2)]

    elif scheme=="triadic":
        colors = [f'hsl({(hsl_vals[0]+120*x)%360},{hsl_vals[1]}%,{hsl_vals[2]}%)' for x in range(3)]

    elif scheme=="quadradic":
        colors = [f'hsl({(hsl_vals[0]+90*x)%360},{hsl_vals[1]}%,{hsl_vals[2]}%)' for x in range(4)]

    elif scheme=="split":
        colors = [f'hsl({(hsl_vals[0]+30*x)%360},{hsl_vals[1]}%,{hsl_vals[2]}%)' for x in range(-1,2)]

    else:
        return "Invalid color scheme"

    return " ".join(new_color_format(colors[x],color_format) for x in range(len(colors)))