class HardwareConstrainedProgramInfo(object):
    def __init__(self, nlines):
        # TODO: determine what statistics we want to take in
        self.nlines = nlines
        pass

    def __str__(self):
        return "number of lines: {}".format(self.nlines)
