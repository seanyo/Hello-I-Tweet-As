#!/usr/bin/env python2

from __future__ import division

import json, httplib, sys

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


labelsPerPage = 8
labelsPerRow = 2
labelWidth = 3.375 * inch
labelHeight = 2.333 * inch
leftMargin = 0.69 * inch
topMargin = 0.59 * inch
horizontalGutter = 0.375 * inch
verticalGutter = 0.19 * inch

headerHeight = 0.75 * inch
footerHeight = 0.125 * inch
bleed = 0.125 * inch

showLabelBoundaries = True


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


c = canvas.Canvas('nametags.pdf', pagesize=letter, bottomup = 0)

users = []
users.append(TwitterUser('seanyo'))
users.append(TwitterUser('chrisonbeer'))
users.append(TwitterUser('andrewphoenix'))


for userNum in range(len(users)):
    c.saveState()

    c.translate(leftMargin + (userNum % labelsPerRow) *
                (labelWidth + horizontalGutter),
                topMargin + (userNum // labelsPerRow) *
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

    c.setFillColorRGB(0, 0, 0)
    x = labelWidth // 2
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
    c.drawCentredString(x, y, '(%s)' % users[userNum].location)

    y += fontSize * 2
    fontSize += 2
    c.setFont("Helvetica-Oblique", fontSize)
    c.drawCentredString(x, y, users[userNum].description)

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
