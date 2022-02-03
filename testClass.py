from Mandelbrot import Mandelbrot


#mandelbrotSet = Mandelbrot()
#mandelbrotSet.run()

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

otherSet = Mandelbrot(
    EQUATION=EQ,
    OUTFILE="other.png",
    IM_RANGE=[(-2, 2), (-2, 2)],
    Z_I=0,
    POINTS=500,
    COLOR_FROM=(0, 0, 0.77),
)

otherSet.run(CLI=False)
