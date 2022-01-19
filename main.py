import numpy as np
import matplotlib.pyplot as plt
from utils import hidePlotBounds, constructBounds
from tqdm import tqdm
from colour import Color
import cmath
import math
from matplotlib import colors

COLOR_TO = (173/255, 216/255, 230/255) # Light Blue
COLOR_FROM = (0, 0, 0) # Black


def log2(x):
	return cmath.log(x, 2)

def sqrt(x):
	return cmath.sqrt(x)

def ComplexModulo(a,b):
	x = a/b
	x = round(x.real) + (round(x.imag)*1j)
	z = x*b
	return a-z

C_RANGE = ((-2, 2), (-2, 2), 10) # ( x ) ( y ) ( num )
ITERATIONS = 100 # Checking than z_n doesn't diverge
fig, ax = plt.subplots(1, 1, figsize=(20,20))

L_POINTS_X = np.linspace(*C_RANGE[0], C_RANGE[2])
L_POINTS_Y = np.linspace(*C_RANGE[1], C_RANGE[2])
POINTS_GRID = np.meshgrid(L_POINTS_X, L_POINTS_Y)
POINTS = []
for i in range(len(POINTS_GRID[0])):
	PX, PY = POINTS_GRID[0][i], POINTS_GRID[1][i]
	POINTS += list(zip(PX, PY))

POINTS = [complex(x, y) for x, y in POINTS]

def generateGradient(from_I, to_I, numPoints=2048):
	cFrom = Color(rgb=from_I)
	cTo = Color(rgb=to_I)
	gradient = list(cFrom.range_to(cTo, numPoints))
	grad_rgb = [x.rgb for x in gradient]
	grad_rgb_255 = [list(map(lambda x: int(x*255), i)) for i in grad_rgb]
	palette = np.array(grad_rgb_255)
	return palette

DEFAULT_COLOR = generateGradient((0, 0, 0), (0, 1, 0))

def determineColor(nDiverge, i, scale=256, clr=DEFAULT_COLOR):
	smoothed = log2(log2(nDiverge**2)/2)
	colors = clr
	colorI = (ComplexModulo(
		math.floor((sqrt(i + 10 - smoothed) * 256).real),
		len(colors)
	)).real
	colorI = math.floor(colorI)
	return colors[colorI], colorI

def generateCmap(boundMap):
	# BoundMap = [ (color, number), ... ]
	BOUNDS_L, COLOR_L = constructBounds(boundMap)
	for i in range(len(COLOR_L)):
		COLOR_L_F = np.array([float(x) for x in COLOR_L[i]], dtype=np.float64)
		COLOR_L[i] = COLOR_L_F / 256.0
	cmap = colors.ListedColormap(COLOR_L)
	norm = colors.BoundaryNorm(BOUNDS_L, cmap.N)
	return cmap, norm

def isBounded(c, iterations=ITERATIONS):
	bounded = True
	z_n = 0
	plotColor = [Color(rgb=(0,0,0)).rgb, 0]
	while bounded and iterations > 0:
		z_n1 = z_n*z_n + c
		if abs(z_n1) > 2:
			bounded=False
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
plt.savefig("out.png")