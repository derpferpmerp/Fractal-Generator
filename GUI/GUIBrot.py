import math

import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from GUIutils import (
    ComplexModulo, generateCmap, generateGradient, hidePlotBounds, log2, sqrt,
)


class Mandelbrot:
    def __init__(
        self,
            COLOR_FROM=(0, 0, 0),
            COLOR_TO=(14/255, 111/255, 125/255),
            POINTS=500,
            IM_RANGE=[(-2, 2), (-2, 2)],
            ITERATIONS=100,
            EQUATION=lambda z, c: z*z + c,
            OUTFILE="Mandelbrot.png",
            GRADUALRATE=2048,
            Z_I=0,
    ):
        '''
        Attributes:
            @param (COLOR_FROM): The First Color in the Gradient
            @param (COLOR_TO)]): The Last Color in the Gradient
            @param (POINTS)]): The Number of Points to Calculate
            @param (IM_RANGE) default=[(-2, 2), (-2, 2)]: The Range for the Imaginary Changing Constant [ RE, IM ]
            @param (ITERATIONS) default=100: The Iteration Limit to Consider c to be bounded
            @param (EQUATION) default=z^2 + c: The Generating Equation
            @param (OUTFILE) default="Mandelbrot.png": The Output file for Graphing
            @param (GRADUALRATE) default=2048: The Number of Swatches in the Color Gradient
        '''
        self.COLOR_FROM = COLOR_FROM
        self.COLOR_TO = COLOR_TO
        self.NUMBER_POINTS = POINTS
        self.C_RANGE = IM_RANGE
        self.C_RANGE.append(POINTS)
        self.ITERATIONS = ITERATIONS
        self.DEFAULT_COLOR = generateGradient(
            COLOR_FROM,
            COLOR_TO,
            numPoints=GRADUALRATE,
        )
        self.GENERATOR = EQUATION
        self.OUTFILE = OUTFILE
        self.Z_I = Z_I

    def determinePoints(self):
        '''
        Function: determinePoints
        Summary: Generates the Numpy Meshgrid for the Mandelbrot Set
        Examples: determinePoints()
        Returns: None
        '''
        self.L_POINTS_X = np.linspace(*self.C_RANGE[0], self.C_RANGE[2])
        self.L_POINTS_Y = np.linspace(*self.C_RANGE[1], self.C_RANGE[2])
        self.POINTS_GRID = np.meshgrid(self.L_POINTS_X, self.L_POINTS_Y)
        self.POINTS = []
        for i in range(len(self.POINTS_GRID[0])):
            PX, PY = self.POINTS_GRID[0][i], self.POINTS_GRID[1][i]
            self.POINTS += list(zip(PX, PY))

        self.POINTS = [complex(x, y) for x, y in self.POINTS]

    def determineColor(self, nDiverge, i, scale=256):
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
        Returns: (Tuple) ( The Color , The Color Index )
        '''
        smoothed = log2(log2(nDiverge*nDiverge)/2)
        colorI = (
            ComplexModulo(
                math.floor((sqrt(i + 10 - smoothed) * scale).real),
                len( self.DEFAULT_COLOR),
            )
        ).real
        colorI = math.floor(colorI)
        return self.DEFAULT_COLOR[colorI], colorI

    def isBounded(self, c, iterations=None):
        '''
        Function: isBounded
        Summary: Evaluates the Mandelbrot Set and assosciates the response with a color
        Examples: isBounded(0 + 1j)
        Attributes:
            @param (c): Complex Number representing the coordinate to evaluate
            @param (iterations) default=ITERATIONS: number of iterations until proven bounded
        Returns: Color
        '''

        if iterations is None:
            iterations = self.ITERATIONS

        bounded = True
        z_n = self.Z_I
        plotColor = [Color(rgb=(0, 0, 0)).rgb, 0]
        while bounded and iterations > 0:
            z_n1 = self.GENERATOR(z_n, c)
            if abs(z_n1) > 2:
                bounded = False
                plotColor = self.determineColor(z_n1, self.ITERATIONS - iterations)
            else:
                z_n = z_n1
            iterations -= 1
        return plotColor


    def process(self, x_i, y_i, GRID, cpoint=0, colorsLST=[]):
        '''
        Function: process
        Summary: Determines the validity of a given point, and applies to a grid for graphing
        Examples: process(0, 0, A_GRID, cpoint=0, colorsLST=[])
        Attributes:
            @param (x_i): The Index of X (would be done through iteration)
            @param (y_i): The Index of Y (would be done through iteration)
            @param (GRID): A Numpy Meshgrid. GRID[x_i, y_i] MUST Exist
            @param (cpoint) default=0: The Current Selected Point (Determined from Indices)
            @param (colorsLST) default=[]: List of Colors
        Returns: Color List, Current Point, Formatted Grid
        '''
        colorR, indR = self.isBounded(self.POINTS[cpoint])
        GRID[x_i, y_i] = indR
        cpoint += 1
        colorsLST.append((colorR, indR))
        return colorsLST, cpoint, GRID

    def run(self, CLI=False, GRAPH=True):
        '''
        Function: run
        Summary: Evaluate the System
        Examples: run()
        Attributes:
            @param (CLI) default=False: Whether or not the user wants a CLI (tqdm progress bar)
            @param (GRAPH) default=True: Whether or not to graph the output
        Returns: Color Map, Boundary Norm
        '''
        self.determinePoints()
        GRID = np.zeros(
            ( self.C_RANGE[2], self.C_RANGE[2]),
            dtype=np.float64,
        )
        cpoint = 0

        colorsL = []
        L_TO_ITER = []
        for x_i in range(self.C_RANGE[2]):
            for y_i in range(self.C_RANGE[2]):
                L_TO_ITER.append([x_i, y_i])

        len(L_TO_ITER) // 2
        C_I = 0
        for x_i, y_i in L_TO_ITER:
            colorsL, cpoint, GRID = self.process(
                x_i, y_i,
                GRID=GRID,
                cpoint=cpoint,
                colorsLST=colorsL,
            )
            C_I += 1
            if C_I % 2 == 0:
                pass
                #sg.one_line_progress_meter('Loading', C_I, MX, 'key', 'Parsing Coordinates')

        cmap, norm = generateCmap(colorsL)
        if GRAPH:
            fig, ax = plt.subplots(1, 1, figsize=(20, 20))
            plt.imshow(GRID, cmap=cmap, norm=norm)
            hidePlotBounds(ax)
            plt.show(
                block=True,
            )
        return GRID, cmap, norm
