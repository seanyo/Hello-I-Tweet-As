#!/usr/bin/env python2

from __future__ import division

import math
try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm


class CalibrationPage:

    (HORIZONTAL, VERTICAL) = range(2)
    (METRIC, IMPERIAL) = range(2)

    def __init__(self):
        self.pageSize = letter

        # The size of the square in the centre of the page should be half of
        # the page height or width, whichever is smaller. This way a second
        # page, folded in half, can be used to verify its size.
        centre_square_size = min(self.pageSize[0], self.pageSize[1]) / 2
        self.centreRectangle = [centre_square_size, centre_square_size]
        self.fudgeLineLength = 2 * inch
        self.fudgeLinePlacement = 2 * inch
        self.fudgeLineCapLength = 0.25 * inch

        # These lines will be rulers printed on the page at roughtly half of
        # the page so that the calibration page can be folded to get the
        # fudge values.
        self.measureLineLength = {CalibrationPage.METRIC: 4 * cm,
                                  CalibrationPage.IMPERIAL: 2 * inch}
        self.measureLinePlacement = 1 * inch

        self.buffer = StringIO()
        c = canvas.Canvas(self.buffer, pagesize=letter, bottomup=False)
        c.setLineWidth(0.2)

        c.setFont('Helvetica', 10)
        c.rect((self.pageSize[0] - self.centreRectangle[0]) / 2,
               (self.pageSize[1] - self.centreRectangle[1]) / 2,
               self.centreRectangle[0], self.centreRectangle[1])

        c.setFont('Helvetica', 7)
        c.line(self.fudgeLinePlacement, 0, self.fudgeLinePlacement, self.fudgeLineLength)
        c.line(self.fudgeLinePlacement - (self.fudgeLineCapLength / 2),
               self.fudgeLineLength,
               self.fudgeLinePlacement + (self.fudgeLineCapLength / 2),
               self.fudgeLineLength)

        c.line(0, self.pageSize[1] - self.fudgeLinePlacement,
               self.fudgeLineLength, self.pageSize[1] - self.fudgeLinePlacement)
        c.line(self.fudgeLineLength,
               self.pageSize[1] - self.fudgeLinePlacement - (self.fudgeLineCapLength / 2),
               self.fudgeLineLength,
               self.pageSize[1] - self.fudgeLinePlacement + (self.fudgeLineCapLength / 2))

        # Top measurement line, in inches
        self.draw_ruler(c, (self.pageSize[0] - self.measureLineLength[CalibrationPage.IMPERIAL]) / 2,
                     self.measureLinePlacement, self.measureLineLength[CalibrationPage.IMPERIAL],
                     units = CalibrationPage.IMPERIAL)

        # Bottom measurement line, in centimetres
        self.draw_ruler(c, (self.pageSize[0] - self.measureLineLength[CalibrationPage.METRIC]) / 2,
                     self.pageSize[1] - self.measureLinePlacement, self.measureLineLength[CalibrationPage.METRIC])

        # Left measurement line, in inches
        self.draw_ruler(c, self.measureLinePlacement,
                     (self.pageSize[1] - self.measureLineLength[CalibrationPage.IMPERIAL]) / 2,
                     self.measureLineLength[CalibrationPage.IMPERIAL], units=CalibrationPage.IMPERIAL,
                     orientation=CalibrationPage.VERTICAL)

        # Right measurement line, in centimetres
        self.draw_ruler(c, self.pageSize[0] - self.measureLinePlacement,
                     (self.pageSize[1] - self.measureLineLength[CalibrationPage.METRIC]) / 2,
                     self.measureLineLength[CalibrationPage.METRIC], orientation=CalibrationPage.VERTICAL)

        c.showPage()
        c.save()

    def draw_ruler(self, canvas, x, y, length, orientation=HORIZONTAL,
                   units=METRIC):

        # Ruler attributes for METRIC and IMPERIAL
        measurements = {
            CalibrationPage.METRIC: {
                'resolution': 0.1 * cm,
                'tick_lengths': [(1, 0.1 * cm),
                                 (10, 0.2 * cm)]
                },
            CalibrationPage.IMPERIAL: {
                'resolution': 0.03125 * inch,
                'tick_lengths': [(1, 0.1 * cm),
                                 (4, 0.15 * cm),
                                 (8, 0.2 * cm),
                                 (16, 0.25 * cm),
                                 (32, 0.3 * cm)]
                }
            }

        canvas.saveState()
        canvas.setLineWidth(0.2)

        if orientation == CalibrationPage.VERTICAL:
            canvas.rotate(90)
            (x, y) = (y, -x)

        canvas.line(x, y, x + length, y)

        tick_placement = x
        settings = measurements[units]
        for tick in range(int(math.ceil(length / settings['resolution'])) + 1):
            for division, size in settings['tick_lengths']:
                if tick % division == 0:
                    tick_length = size
            canvas.line(tick_placement, y, tick_placement, y - tick_length)
            tick_placement += settings['resolution']

        canvas.restoreState()

    def getPDF(self):
        return self.buffer.getvalue()


if __name__ == '__main__':
    p = CalibrationPage()
    print p.getPDF()
