import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
from colour import Color
from numpy import floor
from sympy import E

from main import create as generate


plt.style.use("dark_background")
sg.theme("Black")


def border(elem, CLR="white"):
    return sg.Column([[elem]], background_color=CLR)


class Font:
    def __init__(self, fontName, fontSize=12):
        self.fontSize = str(fontSize)
        self.fontString = fontName
        self.bold = self.BOLD()
        self.italic = self.ITALIC()
        self.underline = self.UNDERLINE()

    def BOLD(self): return (self.fontString + " bold", self.fontSize)

    def ITALIC(self): return (self.fontString + " italic", self.fontSize)

    def UNDERLINE(self): return (self.fontString + " underline", self.fontSize)

    def CUSTOM(self, STR): return (self.fontString + " " + STR, self.fontSize)

    def __call__(self, method=None):
        if method == "bold":
            return self.BOLD()
        elif method == "italic":
            return self.ITALIC()
        elif method == "underline":
            return self.UNDERLINE()
        elif method == None:
            return self.fontString
        else:
            return self.CUSTOM(method)

def recursivelyAdd(lyout, DCT, SLIDER_KEYS={}):
    for k, v in list(DCT.items()):
        SLIDER_KEYS[f"_RIGHT_{k}"] = f"-{k} SLIDER-"
        lyout.append([
            sg.Text(k, auto_size_text=True),
            sg.Slider(
                range=v[0],
                enable_events=True,
                default_value=v[1],
                key=f"-{k} SLIDER-",
                orientation="h",
                size=(20, 10),
                disable_number_display=True,
            ),
            sg.Text(
                str(v[0][1]), key=f"_RIGHT_{k}", font=SLIDER_TEXT(
                "bold",
                ), auto_size_text=True,
            ),
        ])
    return lyout, SLIDER_KEYS

def addTitle(lyout, text):
    lyout.append([
        [sg.Text("_"*30)],
        [
            sg.Text(
                text, size=(10, 1),
                justification="center", font=TITLE_OBJECT("bold"),
            ),
        ],
        [sg.Text("\u00AF"*30)],
    ])
    return lyout

FONT_OBJECT = Font("Helvitica", fontSize=12)
TITLE_OBJECT = Font("Helvitica", fontSize=20)
SLIDER_TEXT = Font("Helvitica", fontSize=8)
BOLD_TITLE = FONT_OBJECT("bold")
presets = {
    "Points": ((250, 1000), 500),
    "Minimum X": ((-2, 0), -2),
    "Maximum X": ((0, 2), 2),
    "Minimum Y": ((-2, 0), -2),
    "Maximum Y": ((0, 2), 2),
}

layout = []
layout = addTitle(layout, "Points Info")
layout, SLIDER_KEYS = recursivelyAdd(layout, presets)
layout = addTitle(layout, "Gradient Info")
layout += [
    [
        sg.In(visible=False, enable_events=True, key="-CLR_IN_K-"),
        sg.ColorChooserButton(
            "Edit the (Initial) Gradient",
            font=SLIDER_TEXT("bold"),
        ),
        sg.Text("", s=(3, 1)),
        sg.Text(
            "( 0, 0, 0 ) | #000000", key="-CLR_IN_TXT-",
            auto_size_text=True, font=SLIDER_TEXT("bold"), text_color="#FFFFFF",
        ),
        border(
            sg.Text(
                " ", key="SWATCH_PREVIEW_IN", font=SLIDER_TEXT(
                "bold",
                ), background_color="black", s=(2, 1), pad=(1, 1),
            ),
        ),
    ],
    [
        sg.In(visible=False, enable_events=True, key="-CLR_OT_K-"),
        sg.ColorChooserButton(
            "Edit the (Final) Gradient",
            font=SLIDER_TEXT("bold"),
        ),
        sg.Text("", s=(3, 1)),
        sg.Text(
            "( 0, 0, 193 ) | #00004d", key="-CLR_OT_TXT-",
            auto_size_text=True, font=SLIDER_TEXT("bold"), text_color="#FFFFFF",
        ),
        border(
            sg.Text(
                " ", key="SWATCH_PREVIEW_OT", font=SLIDER_TEXT(
                "bold",
                ), background_color="#00004d", s=(2, 1), pad=(1, 1),
            ),
        ),
    ],
]

GRADIENT_MANAGER = {
    "Iterations": ((10, 250), 100),
    "Swatches Amount": ((100, 2048), 2048),
}

layout, SLIDER_KEYS = recursivelyAdd(layout, GRADIENT_MANAGER, SLIDER_KEYS=SLIDER_KEYS)

layout = addTitle(layout, "Graphing Info")
layout.append([
    sg.Text("Equation (z, c)", size=(10, 1)),
    sg.InputText("pow(z,2) + c", key="EQ_K", enable_events=True)
])
layout.append([
    sg.Text("Re( Z_I )", size=(10, 1)),
    sg.InputText("0", key="Z_RE", enable_events=True)
])
layout.append([
    sg.Text("Im( Z_I )", size=(10, 1)),
    sg.InputText("0", key="Z_IM", enable_events=True)
])

layout.append([sg.Button("Generate Simulation")])

window = sg.Window(
    title="Fractal Generator",
    layout=layout,
    margins=(100, 50),
    element_justification="center",
)

matplotlibWindowOpen = False

DATA = {
    "INPUT_COLOR": (0.0, 0.0, 0.77),
    "OUTPUT_COLOR": (0.0, 0.0, 0.0),
    "POINTS": 500,
    "IM_RANGE": [[-2, 2], [-2,2]],
    "ITERATIONS": 100,
    "EQUATION": [ lambda z, c: pow(z,2) + c ][0],
    "Z_I": 0,
    "CAMT": 2048
}

while True:
    event, values = window.read()
    if not matplotlibWindowOpen and event == sg.WIN_CLOSED:
        break
    elif event == "Generate Simulation":
        matplotlibWindowOpen = True
        generate(DATA)
        print(event)
    elif matplotlibWindowOpen and event == sg.WIN_CLOSED:
        matplotlibWindowOpen = False
    elif event == "-CLR_IN_K-":
        NEWCOLOR = values["-CLR_IN_K-"]
        fString = window["-CLR_IN_TXT-"].DisplayText
        if NEWCOLOR != "None":
            print(NEWCOLOR)
            clr = Color(NEWCOLOR)
            RGB = floor(np.array(list(clr.rgb)) * 255)
            HEX = clr.hex
            fString = "({:.0f}, {:.0f}, {:.0f}) | {}".format(*RGB, HEX)
            window["SWATCH_PREVIEW_IN"].Update(background_color=HEX)
            DATA["INPUT_COLOR"] = Color(values["-CLR_IN_K-"]).rgb
        window["-CLR_IN_TXT-"].Update(fString)
        print(fString)

        print(DATA)
    elif event == "-CLR_OT_K-":
        NEWCOLOR = values["-CLR_OT_K-"]
        fString = window["-CLR_OT_TXT-"].DisplayText
        if NEWCOLOR != "None":
            print(NEWCOLOR)
            clr = Color(NEWCOLOR)
            RGB = floor(np.array(list(clr.rgb)) * 255)
            HEX = clr.hex
            fString = "({:.0f}, {:.0f}, {:.0f}) | {}".format(*RGB, HEX)
            window["SWATCH_PREVIEW_OT"].Update(background_color=HEX)
            DATA["OUTPUT_COLOR"] = Color(values["-CLR_OT_K-"]).rgb
        window["-CLR_OT_TXT-"].Update(fString)
        print(fString)

        print(DATA)
    elif event == "-Points SLIDER-":
        DATA["POINTS"] = values["-Points SLIDER-"]
    elif event == "-Minimum X SLIDER-":
        MIN = values["-Minimum X SLIDER-"]
        DATA["IM_RANGE"][0][0] = MIN
        window["-Maximum X SLIDER-"].Update(range=(MIN, 10 + MIN))
    elif event == "-Minimum Y SLIDER-":
        MIN = values["-Minimum Y SLIDER-"]
        DATA["IM_RANGE"][1][0] = MIN
        window["-Maximum Y SLIDER-"].Update(range=(MIN, 10 + MIN))
    elif event == "-Maximum X SLIDER-":
        DATA["IM_RANGE"][0][1] = values["-Maximum X SLIDER-"]
    elif event == "-Maximum Y SLIDER-":
        DATA["IM_RANGE"][1][1] = values["-Maximum Y SLIDER-"]
    elif event == "-Initial Z SLIDER-":
        DATA["Z_I"] = values["-Initial Z SLIDER-"]
    elif event in ["Z_IM", "Z_RE"]:
        if not any([ values[x] == "" for x in ["Z_IM", "Z_RE"] ]):
            RE, IM = ( values["Z_RE"], values["Z_IM"] )
            z_part = complex(float(RE), float(IM))
            DATA["Z_I"] = z_part
    elif event == "-Swatches Amount SLIDER-":
        DATA["CAMT"] = values["-Swatches Amount SLIDER-"]
    elif event == "EQ_K":
        DATA["EQUATION"] = lambda z, c: eval(values["EQ_K"].replace("z", z).replace("c", c))
        
    # for k in list(presets.keys()):

    for UTEXT, SLID in list(SLIDER_KEYS.items()):
        if window.Element(UTEXT) == None or values == None or values[SLID] == None:
            continue
        window.Element(UTEXT).Update(int(values[SLID]))

window.close()
