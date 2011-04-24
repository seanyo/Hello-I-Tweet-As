#!/usr/bin/env python2

from __future__ import division

import math

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm


class CalibrationPage:

    (HORIZONTAL, VERTICAL) = range(2)
    (METRIC, IMPERIAL) = range(2)

    def __init__(self):
        self.pageSize = letter

        # We use 4.25" for the centre rectangle so that a letter or legal
        # page folded in half can be used to check its size.
        #
        # TODO: Dynamically set the centre square size from the page size
        self.centreRectangle = [4.25 * inch, 4.25 * inch]
        self.fudgeLineLength = 2 * inch
        self.fudgeLinePlacement = 2 * inch
        self.fudgeLineCapLength = 0.25 * inch

        # These lines will be rulers printed on the page at roughtly half of
        # the page so that the calibration page can be folded to get the
        # fudge values.
        self.measureLineLength = {CalibrationPage.METRIC: 4 * cm,
                                  CalibrationPage.IMPERIAL: 2 * inch}
        self.measureLinePlacement = 1 * inch

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


if __name__ == '__main__':
    c = canvas.Canvas('calibration.pdf', pagesize=letter, bottomup=False)
    p = CalibrationPage()

    c.setFont('Helvetica', 10)
    c.rect((p.pageSize[0] - p.centreRectangle[0]) / 2,
           (p.pageSize[1] - p.centreRectangle[1]) / 2,
           p.centreRectangle[0], p.centreRectangle[1])

    c.setFont('Helvetica', 7)
    c.line(p.fudgeLinePlacement, 0, p.fudgeLinePlacement, p.fudgeLineLength)
    c.line(p.fudgeLinePlacement - (p.fudgeLineCapLength / 2),
           p.fudgeLineLength,
           p.fudgeLinePlacement + (p.fudgeLineCapLength / 2),
           p.fudgeLineLength)

    c.line(0, p.pageSize[1] - p.fudgeLinePlacement,
           p.fudgeLineLength, p.pageSize[1] - p.fudgeLinePlacement)
    c.line(p.fudgeLineLength,
           p.pageSize[1] - p.fudgeLinePlacement - (p.fudgeLineCapLength / 2),
           p.fudgeLineLength,
           p.pageSize[1] - p.fudgeLinePlacement + (p.fudgeLineCapLength / 2))

    # Top measurement line, in inches
    p.draw_ruler(c, (p.pageSize[0] - p.measureLineLength[CalibrationPage.IMPERIAL]) / 2,
                 p.measureLinePlacement, p.measureLineLength[CalibrationPage.IMPERIAL],
                 units = CalibrationPage.IMPERIAL)

    # Bottom measurement line, in centimetres
    p.draw_ruler(c, (p.pageSize[0] - p.measureLineLength[CalibrationPage.METRIC]) / 2,
                 p.pageSize[1] - p.measureLinePlacement, p.measureLineLength[CalibrationPage.METRIC])

    # Left measurement line, in inches
    p.draw_ruler(c, p.measureLinePlacement,
                 (p.pageSize[1] - p.measureLineLength[CalibrationPage.IMPERIAL]) / 2,
                 p.measureLineLength[CalibrationPage.IMPERIAL], units=CalibrationPage.IMPERIAL,
                 orientation=CalibrationPage.VERTICAL)

    # Right measurement line, in centimetres
    p.draw_ruler(c, p.pageSize[0] - p.measureLinePlacement,
                 (p.pageSize[1] - p.measureLineLength[CalibrationPage.METRIC]) / 2,
                 p.measureLineLength[CalibrationPage.METRIC], orientation=CalibrationPage.VERTICAL)

    c.showPage()
    c.save()
