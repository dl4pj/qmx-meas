from my_types import Mode

class MeasConfig:
    def __init__(self, fvfo, mode):
        self.fvfo = fvfo
        self.mode = mode
        self.span = 10e3
        if self.mode == Mode.LSB:
            self.tl = -1900
            self.tr = -700
        else:
            self.tl = 700
            self.tr = 1900
        self.ipl = 2*self.tl - self.tr
        self.ipr = 2*self.tr -self.tl
        self.fl = self.fvfo + self.tl
        self.fr = self.fvfo + self.tr
        self.fc = (self.fl + self.fr) // 2
        self.fipl = self.fvfo + self.ipl
        self.fipr = self.fvfo + self.ipr
        self.fstart = self.fc - self.span/2
        self.fstop = self.fc + self.span/2