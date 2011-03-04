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
        self.fudgeLineCapLength = 0.25 * inch


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

    c.showPage()
    c.save()
