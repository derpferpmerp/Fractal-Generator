from commonEq import carpetFractal


class QualityPreset:
    def __init__(self, name, points, iterations):
        self.name = name
        self.points = points
        self.iterations = iterations

    def iterate(self):
        return [("POINTS", self.points), ("ITERATIONS", self.iterations)]

class ColorPreset:
    def __init__(self, COLOR_FROM, COLOR_TO, CAMT):
        self.COLOR_FROM = COLOR_FROM
        self.COLOR_TO = COLOR_TO
        self.CAMT = CAMT

    def iterate(self):
        return [("CAMT", self.CAMT), ("INPUT_COLOR", self.COLOR_FROM), ("OUTPUT_COLOR", self.COLOR_TO)]

class EquationPreset:
    def __init__(self, equation, im_range, z_i):
        self.Z_I = z_i
        self.IM_RANGE = im_range
        self.EQUATION = equation

    def iterate(self):
        return [("Z_I", self.Z_I), ("IM_RANGE", self.IM_RANGE), ("EQUATION", self.EQUATION)]

class FullPreset:
    def __init__(self, eqPreset: EquationPreset, clrPreset: ColorPreset, quaPreset: QualityPreset, name: str):
        self.eqResponse = eqPreset.iterate()
        self.clrResponse = clrPreset.iterate()
        self.quaResponse = quaPreset.iterate()
        self.name = name

    def iterate(self):
        return [self.name, self.eqResponse + self.clrResponse + self.quaResponse]

class SmartPreset(FullPreset):
    def __init__(self, EQ=None, CLR=None, QUA=None, NAME=None):

        if not isinstance(EQ, EquationPreset): self.EQ = EquationPreset(carpetFractal, [[-2, 2], [-2, 2]], 0)
        else: self.EQ = EQ

        if not isinstance(CLR, ColorPreset): self.CLR = SMOOTH_BLUE
        else: self.CLR = CLR

        if not isinstance(QUA, QualityPreset): self.QUA = HQ_QUALITY
        else: self.QUA = QUA

        if type(NAME) != "string": self.NAME = "Carpet"
        else: self.NAME = NAME
        
        FullPreset.__init__(self, self.EQ, self.CLR, self.QUA, self.NAME)

    def setQuality(self, QUA):
        FullPreset.__init__(self, self.EQ, self.CLR, QUA, self.NAME)

    def setEquation(self, EQ):
        FullPreset.__init__(self, EQ, self.CLR, self.QUA, self.NAME)

    def setColor(self, CLR):
        FullPreset.__init__(self, self.EQ, CLR, self.QUA, self.NAME)


HQ_QUALITY = QualityPreset("HQ", 1250, 100)
HD_QUALITY = QualityPreset("HD", 100, 100)
MD_QUALITY = QualityPreset("MD", 850, 100)
LQ_QUALITY = QualityPreset("LQ", 500, 100)

SMOOTH_BLUE = ColorPreset((0.0, 0.0, 0.77), (14/255, 111/255, 125/255), 2048)

CARPET = SmartPreset(NAME="Carpet")
