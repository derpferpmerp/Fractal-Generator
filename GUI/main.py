from GUIBrot import Mandelbrot


def iMult(num):
    re = num.real
    im = num.imag
    return complex(-1 * im, re)

SMART_Z = complex( pow(10,-4), pow(10,-4))

def EQ(z, c):
    a, b = ( c.real, c.imag)
    x, y = ( z.real, z.imag)
    #return pow( pow(z,2) + pow(c, 2), 2 * z )
    return z * z + c

def create(DICT_DATA):
    COLOR_FROM = DICT_DATA["INPUT_COLOR"]
    COLOR_TO = DICT_DATA["OUTPUT_COLOR"]
    POINTS = DICT_DATA["POINTS"]
    IM_RANGE = DICT_DATA["IM_RANGE"]
    ITERATIONS = DICT_DATA["ITERATIONS"]
    EQUATION = DICT_DATA["EQUATION"]
    GRADUALRATE = DICT_DATA["CAMT"]
    Z_I = DICT_DATA["Z_I"]
    print(DICT_DATA)
    SET = Mandelbrot(
        EQUATION=EQUATION,
        IM_RANGE=IM_RANGE,
        Z_I=Z_I,
        POINTS=POINTS,
        COLOR_FROM=COLOR_FROM,
        COLOR_TO=COLOR_TO,
        GRADUALRATE=GRADUALRATE,
        ITERATIONS=ITERATIONS,
    )

    SET.run(CLI=False)
