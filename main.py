import cmath
import math

import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from matplotlib import colors
from tqdm import tqdm

from utils import constructBounds, hidePlotBounds

COLOR_TO = (14/255, 111/255, 125/255)              # Light Blue
COLOR_FROM = (0, 0, 0)                             # Black
NUMBER_POINTS = 500                                # Side Length of Square
C_RANGE = ((-2, 2), (-2, 2), NUMBER_POINTS)        # ( x ) ( y ) ( num )
ITERATIONS = 100                                   # Checking than z_n doesn't diverge


fig, ax = plt.subplots(1, 1, figsize=(20, 20))


def log2(x):
	'''
	Function: log2
	Summary: Returns the Base 2 Logarithm of a complex number
	Examples: log2(complex(1,0))
	Attributes: 
			@param (x): Complex Number Input
	Returns: Complex Number
	'''
	return cmath.log(x, 2)


def sqrt(x):
	'''
	Function: sqrt
	Summary: Returns the Square Root of a Complex Number
	Examples: sqrt(complex(1,1))
	Attributes: 
			@param (x): The Complex Number to Root
	Returns: Complex Number
	'''
	return cmath.sqrt(x)


def ComplexModulo(a, b):
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


L_POINTS_X = np.linspace(*C_RANGE[0], C_RANGE[2])
L_POINTS_Y = np.linspace(*C_RANGE[1], C_RANGE[2])
POINTS_GRID = np.meshgrid(L_POINTS_X, L_POINTS_Y)
POINTS = []
for i in range(len(POINTS_GRID[0])):
	PX, PY = POINTS_GRID[0][i], POINTS_GRID[1][i]
	POINTS += list(zip(PX, PY))

POINTS = [complex(x, y) for x, y in POINTS]


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


DEFAULT_COLOR = generateGradient(COLOR_FROM, COLOR_TO)


def determineColor(nDiverge, i, scale=256, clr=DEFAULT_COLOR):
	'''
	Function: determineColor
	Summary: Evaluates the Color for the given Pixel in the Mandelbrot Set
	Examples: determineColor((0+4j), 0)
	Attributes: 
			@param (nDiverge): The Complex Coordinate where the Pixel Diverged
			@param (i): The Number of Iterations from the Pixel
			@param (scale) default=256:
					Max Color Value + 1 from Color Array
					(256 = RGB MAX + 1 = 255 + 1)
			@param (clr) default=DEFAULT_COLOR: The Color Swatches to Choose From
	Returns: InsertHere
	'''
	smoothed = log2(log2(nDiverge*nDiverge)/2)
	colors = clr
	colorI = (ComplexModulo(
		math.floor((sqrt(i + 10 - smoothed) * 256).real),
		len(colors)
	)).real
	colorI = math.floor(colorI)
	return colors[colorI], colorI


def generateCmap(boundMap):
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
		COLOR_L[i] = COLOR_L_F / 256.0
	cmap = colors.ListedColormap(COLOR_L)
	norm = colors.BoundaryNorm(BOUNDS_L, cmap.N)
	return cmap, norm


def isBounded(c, iterations=ITERATIONS):
	'''
	Function: isBounded
	Summary: Evaluates the Mandelbrot Set and assosciates the response with a color
	Examples: isBounded(0 + 1j)
	Attributes: 
			@param (c): Complex Number representing the coordinate to evaluate
			@param (iterations) default=ITERATIONS: number of iterations until proven bounded
	Returns: Color
	'''
	bounded = True
	z_n = 0
	plotColor = [Color(rgb=(0, 0, 0)).rgb, 0]
	while bounded and iterations > 0:
		z_n1 = z_n*z_n + c
		if abs(z_n1) > 2:
			bounded = False
			plotColor = determineColor(z_n1, ITERATIONS - iterations)
		else:
			z_n = z_n1
		iterations -= 1
	return plotColor


GRID = np.zeros((C_RANGE[2], C_RANGE[2]), dtype=np.float64)
cpoint = 0

colorsL = []
with tqdm(total=C_RANGE[2]**2) as pbar:
	for x_i in range(C_RANGE[2]):
		for y_i in range(C_RANGE[2]):
			colorR, indR = isBounded(POINTS[cpoint])
			GRID[x_i, y_i] = indR
			cpoint += 1
			colorsL.append((colorR, indR))
			pbar.update(1)

cmap, norm = generateCmap(colorsL)


plt.imshow(GRID, cmap=cmap, norm=norm)
hidePlotBounds(ax)
<<<<<<< HEAD
plt.savefig("out.png")
=======
plt.savefig(
	"out.png",
	bbox_inches='tight',
	pad_inches=0,
	format='png',
)
>>>>>>> 0f59623de8d57ffc5304a452a1df967577fd2d35
