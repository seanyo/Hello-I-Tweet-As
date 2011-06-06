#!/usr/bin/env python2

from __future__ import division

import argparse, json, httplib, sys
try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader


class TwitterUser:
    twitterHost = 'api.twitter.com'
    twitterPort = 80

    def __init__(self, userName):
        self.userName = userName
        self.sync()

    def sync(self):
        conn = httplib.HTTPConnection(TwitterUser.twitterHost)
        request = '/1/users/show/{0}.json'.format(self.userName)
        conn.request('GET', request)
        response = conn.getresponse()

        if response.status == 200:
            user = json.loads(response.read())
            self.userName = user[u'screen_name']  # Capitalization may change
            self.name = user[u'name']
            self.location = user[u'location']
            self.avatarUrl = \
                user[u'profile_image_url'].replace('normal', 'bigger')
            self.description = user[u'description']
            self.verified = user[u'verified']


class LabelFormat:
    '''A class to represent the layout of a sheet of labels.'''
    def __init__(self, labels_per_page=8, labels_per_row=2,
                 label_width=3.375 * inch, label_height=(2 + 1/3) * inch,
                 left_margin=(11 / 16) * inch, top_margin=(19 / 32) * inch,
                 horizontal_gutter=0.375 * inch, vertical_gutter=(3/16 * inch),

                 header_height=0.75 * inch, footer_height=0.125 * inch,
                 bleed=0.125 * inch, padding=0.25 * inch):

        '''Default to Avery 8-up nametag settings, e.g. #8395, 5395, or
        ##45395.'''
        self.labelsPerPage = labels_per_page
        self.labelsPerRow = labels_per_row
        self.labelWidth = label_width
        self.labelHeight = label_height
        self.leftMargin = left_margin
        self.topMargin = top_margin
        self.horizontalGutter = horizontal_gutter
        self.verticalGutter = vertical_gutter

        self.headerHeight = header_height
        self.footerHeight = footer_height
        self.bleed = bleed
        self.padding = padding


class LabelBuilder:

    @classmethod
    def wrapText(cls, canvas, text, maxWidth, maxLines=None, append=u'...'):
        words = text.split(' ')
        currentWordIndex = 0
        lines = []

        while currentWordIndex < len(words):
            currentLine = words[currentWordIndex]
            currentWordIndex += 1
            while currentWordIndex + 1 < len(words) and \
                    canvas.stringWidth(currentLine + " " + \
                                           words[currentWordIndex + 1]) < maxWidth:
                currentLine += ' ' + words[currentWordIndex]
                currentWordIndex += 1

            lines.append(currentLine)

        if maxLines is not None and maxLines < len(lines):
            lines = lines[:maxLines]
            while canvas.stringWidth(lines[maxLines-1] + append) > maxWidth:
                # Remove words from the end until there's room for "..."
                lines[maxLines-1] = lines[maxLines-1].rsplit(' ', 1)[0]
            lines[maxLines-1] += append

        return lines

    def __init__(self, format):
        self.format = format
        self.users = []
        self.fudge = [0, 0]
        self.buffer = StringIO()
        self.canvas = canvas.Canvas(self.buffer,
                                    pagesize=letter,
                                    bottomup = 0)
        self.canvas.setTitle('Nametags')
        self.canvas.setCreator('I Tweet As -- http://itweet.as/')

    def overlayLabelBoundaries(self):
        self.canvas.setDash(6, 3)
        self.canvas.setStrokeColorCMYK(0.0, 0.0, 0.0, 0.75)
        self.canvas.setLineWidth(0.5)

        x = self.format.leftMargin
        y = self.format.topMargin
        for row in range(self.format.labelsPerPage //
                         self.format.labelsPerRow):
            for label in range(self.format.labelsPerRow):
                self.canvas.roundRect(x, y, self.format.labelWidth,
                                      self.format.labelHeight, 0.125 * inch)
                x = x + self.format.labelWidth + self.format.horizontalGutter
            x = self.format.leftMargin
            y = y + self.format.labelHeight + self.format.verticalGutter

    def addUser(self, user):
        self.users.append(user)

    def setFudge(self, horizontal, vertical):
        self.format.leftMargin += int(horizontal)
        self.format.topMargin += int(vertical)

    def generatePDF(self, offset=0, showLabelBoundaries=False):
        c = self.canvas

        for userNum in range(len(self.users)):
            if userNum != 0 and (userNum + offset) % self.format.labelsPerPage == 0:
                if showLabelBoundaries:
                    self.overlayLabelBoundaries()
                c.showPage()

            c.saveState()

            c.translate(self.format.leftMargin +
                                  ((userNum + offset) %
                                   self.format.labelsPerRow) *
                                  (self.format.labelWidth +
                                   self.format.horizontalGutter),
                                  self.format.topMargin +
                                  ((userNum + offset) %
                                   self.format.labelsPerPage //
                                   self.format.labelsPerRow) *
                                  (self.format.labelHeight +
                                   self.format.verticalGutter))

            c.setFillColorCMYK(0.0, 0.95, 0.95, 0.20);
            c.setStrokeColorCMYK(0.0, 0.95, 0.95, 0.20)
            c.roundRect(0 - self.format.bleed, 0 - self.format.bleed,
                                  self.format.labelWidth +
                                  2 * self.format.bleed,
                                  self.format.labelHeight +
                                  2 * self.format.bleed,
                                  0.125*inch, stroke=0, fill=1)
            c.setFillColorCMYK(0.0, 0.0, 0.0, 0.0);
            self.canvas.rect(0 - self.format.bleed, self.format.headerHeight,
                             self.format.labelWidth + 2 * self.format.bleed,
                             self.format.labelHeight -
                             self.format.headerHeight -
                             self.format.footerHeight,
                   stroke=0, fill=1)

            c.setFillColorCMYK(0.0, 0.0, 0.0, 0.0)

            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(
                self.format.labelWidth // 2, 0.375 * inch, "HELLO")

            c.setFont("Helvetica-Bold", 20)
            c.drawCentredString(self.format.labelWidth // 2,
                                          0.625 * inch, "I TWEET AS")

            image = ImageReader(self.users[userNum].avatarUrl)
            # Images print upside down if c.bottomup is False, so flip them
            c.saveState()
            c.scale(1.0, -1.0)
            c.drawImage(image, 0.25 * inch, -1.875 * inch,
                                    0.75 * inch, 0.75 * inch)
            c.restoreState()

            c.setFillColorCMYK(0.0, 0.0, 0.0, 1.0)
            x = (self.format.labelWidth - 0.75 * inch -
                 3 * self.format.padding) // \
                 2 + 0.75 * inch + 2 * self.format.padding
            y = 1.125 * inch
            fontSize = 16

            c.setFont("Helvetica-Bold", fontSize)
            c.drawCentredString(x, y, '@{0}'.format(self.users[userNum].userName))

            y += fontSize
            fontSize -= 2
            c.setFont("Helvetica", fontSize)
            c.drawCentredString(x, y, self.users[userNum].name)

            y += fontSize
            fontSize -= 3
            c.setFont("Helvetica", fontSize)
            c.drawCentredString(x, y, self.users[userNum].location)

            y += fontSize * 2
            fontSize += 2
            c.setFont("Helvetica-Oblique", fontSize)
            lines = LabelBuilder.wrapText(c, self.users[userNum].description,
                                          self.format.labelWidth - 0.75 * inch -
                                          3 * self.format.padding, 2)
            for line in lines:
                c.drawCentredString(x, y, line)
                y += fontSize

            if self.users[userNum].verified:
                c.saveState()
                c.scale(1.0, -1.0)
                c.drawImage('html/images/verified.png', 0.875 * inch, -2 * inch,
                            0.25 * inch, 0.25 * inch, mask=[0,1,0,1,0,1])
                c.restoreState()

            c.restoreState()

        if showLabelBoundaries:
            self.overlayLabelBoundaries()

        c.showPage()
        c.save()

    def getPDF(self):
        return self.buffer.getvalue()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make Twitter nametags')
    parser.add_argument('usernames', metavar='username', nargs='+',
                        help='Twitter usernames')
    parser.add_argument('--overlay-boundaries', dest='showLabelBoundaries',
                        action='store_true', help='Overlay label boundaries')
    parser.add_argument('--offset', dest='labelOffset', metavar='N', type=int,
                        default=0, help='Skip N labels')
    parser.add_argument('--fudge', dest='fudge', help='Fudge factor in points',
                        type=int, nargs=2, metavar=('horiz', 'vert'))
    args = parser.parse_args()

    builder = LabelBuilder(LabelFormat())

    # Adjust the overall registration to correct for printer quirkiness
    if args.fudge is not None:
        builder.setFudge(args.fudge[0], args.fudge[1])

    users = []
    for username in args.usernames:
        builder.addUser(TwitterUser(username))

    builder.generatePDF(offset=args.labelOffset)

    print builder.getPDF()
