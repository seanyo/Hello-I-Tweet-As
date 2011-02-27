#!/usr/bin/env python2

from __future__ import division

import json, httplib, sys

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader


labelsPerPage = 8
labelsPerRow = 2
labelWidth = 3.375 * inch
labelHeight = (2 + 1/3) * inch
leftMargin = (11 / 16) * inch
topMargin = (19 / 32) * inch
horizontalGutter = 0.375 * inch
verticalGutter = (5.5 / 32) * inch

headerHeight = 0.75 * inch
footerHeight = 0.125 * inch
bleed = 0.125 * inch
padding = 0.25 * inch

showLabelBoundaries = True
labelOffset = 1


class TwitterUser:
    twitterHost = 'api.twitter.com'
    twitterPort = 80

    def __init__(self, userName):
        self.userName = userName
        self.sync()

    def sync(self):
        conn = httplib.HTTPConnection(TwitterUser.twitterHost)
        request = '/1/users/show/%s.json' % self.userName
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


def wrapText(canvas, text, maxWidth, maxLines=None, append=u'...'):
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


c = canvas.Canvas('nametags.pdf', pagesize=letter, bottomup = 0)
c.setTitle('Nametags')
c.setCreator('I Tweet As -- http://itweet.as/')

users = []
users.append(TwitterUser('seanyo'))
users.append(TwitterUser('chrisonbeer'))
users.append(TwitterUser('andrewphoenix'))


for userNum in range(len(users)):
    c.saveState()

    c.translate(leftMargin + ((userNum + labelOffset) % labelsPerRow) *
                (labelWidth + horizontalGutter),
                topMargin + ((userNum + labelOffset) // labelsPerRow) *
                (labelHeight + verticalGutter))

    c.setFillColorRGB(0xff / 0xcc, 0, 0);
    c.setStrokeColorRGB(0xff / 0xcc, 0, 0)
    c.roundRect(0 - bleed, 0 - bleed,
                labelWidth + 2*bleed, labelHeight + 2*bleed,
                0.125*inch, stroke=0, fill=1)
    c.setFillColorRGB(0xfff, 0xfff, 0xfff);
    c.rect(0-bleed, headerHeight,
           labelWidth + 2*bleed, labelHeight - headerHeight - footerHeight,
           stroke=0, fill=1)

    c.setFillColorRGB(0xff, 0xff, 0xff)

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(labelWidth // 2, 0.375 * inch, "HELLO")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(labelWidth // 2, 0.625 * inch, "I TWEET AS")

    image = ImageReader(users[userNum].avatarUrl)
    # Images print upside down if c.bottomup is False, so flip them
    c.saveState()
    c.scale(1.0, -1.0)
    c.drawImage(image, 0.25 * inch, -1.875 * inch, 0.75 * inch, 0.75 * inch)
    c.restoreState()

    c.setFillColorRGB(0, 0, 0)
    x = (labelWidth - 0.75 * inch - 3 * padding) // \
        2 + 0.75 * inch + 2 * padding
    y = 1.125 * inch
    fontSize = 16

    c.setFont("Helvetica-Bold", fontSize)
    c.drawCentredString(x, y, '@%s' % users[userNum].userName)

    y += fontSize
    fontSize -= 2
    c.setFont("Helvetica", fontSize)
    c.drawCentredString(x, y, users[userNum].name)

    y += fontSize
    fontSize -= 3
    c.setFont("Helvetica", fontSize)
    c.drawCentredString(x, y, users[userNum].location)

    y += fontSize * 2
    fontSize += 2
    c.setFont("Helvetica-Oblique", fontSize)
    lines = wrapText(c, users[userNum].description,
                     labelWidth - 0.75 * inch - 3 * padding, 2)
    for line in lines:
        c.drawCentredString(x, y, line)
        y += fontSize

    c.restoreState()


# Overlay label boundaries on the page
if showLabelBoundaries:
    c.setDash(6, 3)
    c.setStrokeColorRGB(0.25, 0.25, 0.25)
    c.setLineWidth(0.5)

    x = leftMargin
    y = topMargin
    for row in range(labelsPerPage // labelsPerRow):
        for label in range(labelsPerRow):
            c.roundRect(x, y, labelWidth, labelHeight, 0.125 * inch)
            x = x + labelWidth + horizontalGutter
        x = leftMargin
        y = y + labelHeight + verticalGutter

c.showPage()
c.save()
