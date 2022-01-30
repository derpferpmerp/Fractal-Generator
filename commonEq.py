import cmath
from cmath import atan, cos, exp
from cmath import log as ln
from cmath import pi as PI
from cmath import sin, sqrt, tan

def spiralMandelbrot(z, c):
    return (z + c) * (z + c) + (z + c)

def dualMandelbrot(z, c):
    return z*z*z + c

def antBrot(z, c):
    return (z*z - z)*(z*z - z) + c

def shoeFractal(z, c):
    return complex(
        z.real * z.real + z.real * z.imag + c.real,
        z.imag * z.imag - z.real * z.imag + c.imag
    )

# Num 87
def arrowFractal(z, c):
    a, b = ( c.real, c.imag )
    x, y = ( z.real, z.imag )
    return complex(
        pow(x,3) - y * pow(x,2) + x * pow(y,2) - x*y + a,
        pow(y,3) - x * pow(y,2) + y * pow(x,2) + x*y + b
    )
    
# Horn Fractal??
def hornFractal(z, c):
    z_i = complex(pow(10,-4),pow(10,-4))
    return z_i, z * tan(ln(z)) + c,

# Force Field
def forceFieldFractal(z, c):
    z_i = complex(pow(10,-4),pow(10,-4))
    return z_i, (z * ln(z))/(exp(c))

# Feather Duster Set
def featherDuster(z, c):
    if z.real == 0:
        theta = PI / 2
    else:
        theta = atan(z.imag / z.real)
    return sqrt(pow(z,4) + cos(theta) + c)

# Carpet
# 10/10 With 1250 Points C_I = (0, 0, 0.77)
def EQ(z, c):
    a, b = ( c.real, c.imag )
    x, y = ( z.real, z.imag )
    #return pow( pow(z,2) + pow(c, 2), 2 * z )
    return z * z * sin(x) + c * z * y + z * z * cos(x) + c * z * sin(y) + c

