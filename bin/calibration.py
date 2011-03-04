#!/usr/bin/env python2

from __future__ import division

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


class CalibrationPage:

    def __init__(self):
        self.pageSize = letter
        self.centreRectangle = [3 * inch, 3 * inch]
        self.fudgeLineLength = 2 * inch
        self.fudgeLinePlacement = 2 * inch


if __name__ == '__main__':
    c = canvas.Canvas('calibration.pdf', pagesize=letter, bottomup=False)
    p = CalibrationPage()

    c.setFont('Helvetica', 10)
    c.rect((p.pageSize[0] - p.centreRectangle[0]) / 2,
           (p.pageSize[1] - p.centreRectangle[1]) / 2,
           p.centreRectangle[0], p.centreRectangle[1])

    c.setFont('Helvetica', 7)
    c.line(p.fudgeLinePlacement, 0, p.fudgeLinePlacement, p.fudgeLineLength)
    for tick in range(0, int(p.fudgeLineLength) + 1, 3):
        if tick % 12 == 0:
            offset = 6
            c.drawRightString(p.fudgeLinePlacement - 12, tick + 2,
                              '{0}'.format(tick - 72))
        else:
            offset = 3
        c.line(tick, p.pageSize[1] - p.fudgeLinePlacement - offset,
               tick, p.pageSize[1] - p.fudgeLinePlacement)

    c.line(0, p.pageSize[1] - p.fudgeLinePlacement,
           p.fudgeLineLength, p.pageSize[1] - p.fudgeLinePlacement)
    for tick in range(0, int(p.fudgeLineLength) + 1, 3):
        if tick % 12 == 0:
            offset = 6
            c.saveState()
            c.rotate(270)
            c.drawString(-p.pageSize[1] + p.fudgeLinePlacement + 12, tick + 2,
                          '{0}'.format(tick - 72))
            c.restoreState()
        else:
            offset = 3
        c.line(p.fudgeLinePlacement - offset, tick,
               p.fudgeLinePlacement, tick)

    c.showPage()
    c.save()
