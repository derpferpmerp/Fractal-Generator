import cmath
import math

import numpy as np
from colour import Color
from matplotlib.colors import BoundaryNorm, ListedColormap


def hidePlotBounds(ax):
    '''
    Function: hidePlotBounds
    Summary: Hides the Matplotlib Plot Bounds
    Examples: hidePlotBounds(plt)
    Attributes:
        @param (ax): Matplotlib Axis Object
    Returns: None
    '''
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.set_xticks([])
    ax.set_yticks([])

    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)

def constructBounds(lst, tau=0.1):
    '''
    Function: constructBounds
    Summary: Generates the Bounds for the Boundary Norm
    Attributes:
        @param (lst):
            Description: Data List for Input
            Format: [ ( ( R, G, B ), INDX ) ... ]
        @param (tau) default=0.1:
            Description: Mult of Distance for Spacing,
            Format: D*(1-tau) < D < D*(1+tau)
    Returns: Boundary List, Color List
    '''
    # LST : [ ( ( R, G, B ), INDX ) ... ]
    # Tau : Mult of Distance for Spacing, D*(1-tau) < D < D*(1+tau)
    lstSorted = sorted(lst, key=lambda x: x[1])
    lstSorted = [ (x[0], x[1] * np.array([1-tau, 1+tau])) for x in lstSorted]
    FINALBOUNDS = []
    FINALCOLORS = []
    for i in range(len(lstSorted)):
        item = lstSorted[i]
        if i > 0:
            if sorted(item[0]) == sorted(FINALCOLORS[-1]):
                continue

        if i == 0:
            FINALBOUNDS.append(item[1][0])
        elif i == len(lstSorted) - 1:
            FINALBOUNDS.append(item[1][0])
            FINALBOUNDS.append(item[1][-1])
        else:
            I = item[1][0]
            if I != FINALBOUNDS[-1]:
                FINALBOUNDS.append(item[1][0])
        FINALCOLORS.append(item[0])
    return FINALBOUNDS, FINALCOLORS

def log2(x:complex):
    '''
    Function: log2
    Summary: Returns the Base 2 Logarithm of a complex number
    Examples: log2(complex(1,0))
    Attributes:
        @param (x): Complex Number Input
    Returns: Complex Number
    '''
    return cmath.log(x, 2)


def sqrt(x:complex):
    '''
    Function: sqrt
    Summary: Returns the Square Root of a Complex Number
    Examples: sqrt(complex(1,1))
    Attributes:
        @param (x): The Complex Number to Root
    Returns: Complex Number
    '''
    return cmath.sqrt(x)


def ComplexModulo(a:complex, b:complex):
    '''
    Function: ComplexModulo
    Summary: Completes a Modulo in the Imaginary and Real Dimensions
    Examples: ComplexModulo(4 + 4j, 2)
    Format: "a mod b" -> ComplexModulo(a,b)
    Attributes:
        @param (a): First Term
        @param (b): Second Term
    Returns: Complex Number
    '''
    x = a/b
    x = math.floor(x.real) + (math.floor(x.imag)*1j)
    z = x*b
    return a-z

def generateGradient(from_I, to_I, numPoints=2048):
    '''
    Function: generateGradient
    Summary: Generates a color gradient
    Examples: generateGradient( (0, 0, 0), (1, 1, 1) )
    Attributes:
        @param (from_I): RGB Tuple (Starting Point of Gradient)
        @param (to_I):   RGB Tuple (Ending Point of Gradient)
        @param (numPoints) default=2048: Number of Steps in Gradient
    Returns: Numpy Array of RGB Values
    '''
    cFrom = Color(rgb=from_I)
    cTo = Color(rgb=to_I)
    gradient = list(cFrom.range_to(cTo, numPoints))
    grad_rgb_255 = []
    for x in gradient:
        RGB = 255 * np.array(x.rgb)
        RGB = np.array(RGB, dtype=int)
        grad_rgb_255.append(RGB)
    palette = np.array(grad_rgb_255)
    return palette

def generateCmap(boundMap, scale=256.0):
    '''
    Function: generateCmap
    Summary: Converts Boundary Map to Color Map and Norm
    Examples: generateCmap( ((R, G, B), 200), ... )
    Attributes:
        @param (boundMap):
            Description: Bounaries Corresponding to the Colors
            Format: [ (color, number), ... ]
    Returns: ListedColormap, BoundaryNorm
    '''

    BOUNDS_L, COLOR_L = constructBounds(boundMap)
    for i in range(len(COLOR_L)):
        COLOR_L_F = np.array([float(x) for x in COLOR_L[i]], dtype=np.float64)
        COLOR_L[i] = COLOR_L_F / scale
    cmap = ListedColormap(COLOR_L)
    norm = BoundaryNorm(BOUNDS_L, cmap.N)
    return cmap, norm
