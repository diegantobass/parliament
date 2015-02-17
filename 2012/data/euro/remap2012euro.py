#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

filepath = sys.argv[1]
with open(filepath, 'r') as xml_file:
    xml = xml_file.read()

drawMap = False
if len(sys.argv) > 2:
    drawMap = True

page = 0
topvals = {}
leftvals = {}
maxtop = 1300
results = []
headers = ['candidat', 'depensestotales', 'recettestotales', 'dons', 'appartspartis', 'concoursnature', 'autres', 'perso', 'soldescompte', 'DEV', 'RFE', 'DECCNCCFP']
record = ["", "", "", "", "", "","", "", "","", "", "", ""]
re_line = re.compile(r'<page number|text top="(\d+)" left="(-?)(\d+)"[^>]*font="(\d+)">(.*)</text>', re.I)
save = False
for line in (xml).split("\n"):
    #print "DEBUG %s" % line
    if line.startswith('<page'):
        page += 1
    if not line.startswith('<text'):
        continue
    attrs = re_line.search(line)
    if not attrs or not attrs.groups():
        #print "WARNING : line detected with good font but wrong format %s" % line
        continue
    font = int(attrs.group(4))
    top = int(attrs.group(1))

    if page < 6:
        continue

    if top > maxtop:
        continue

    if not font in topvals:
        topvals[font] = []
    topvals[font].append(top)

    if attrs.group(2):
        left = int(attrs.group(3)) + 892
    else :
        left = int(attrs.group(3))

    if not font in leftvals:
        leftvals[font] = []
    leftvals[font].append(left)

    if drawMap:
        continue

    text = attrs.group(5).replace("&amp;", "&")
    #print "DEBUG %s %s %s %s" % (font, left, top, text)

    # Nom du candidats
    if left < 250:
        results.append(record)
        record = ["", "", "", "", "", "","", "", "","", "", "", ""]
        record[0] += text + '\r'

    # Dépenses totales
    elif left < 320:
        record[1] += text + '\r'

    # Recettes totales
    elif left < 365:
        record[2] += text + '\r'

    # Dons
    elif left < 420:
        record[3] += text + '\r'

    # Apports partis
    elif left < 465:
        record[4] += text + '\r'

    # Concours en nature
    elif left < 515:
        record[5] += text + '\r'

    # Autres
    elif left < 567:
        record[6] += text + '\r'

    # Apports personnels
    elif left < 620:
        record[7] += text + '\r'

    # Solde compte de campagne
    elif left < 670:
        record[8] += text + '\r'

    # DEV
    elif left < 725:
        record[9] += text + '\r'

    # RFE
    elif left < 775:
        record[10] += text + '\r'

    # Dec CNCCFP
    elif left < 800:
        record[11] += text + '\r'



if not drawMap:
    print ",".join(['"%s"' % h for h in headers])
    for i in results:
        for j in range(len(i)):
            i[j] = i[j].replace('<b>', '').replace('</b>', '').strip()
        print ",".join([str(i[a]) if isinstance(i[a], int) else "\"%s\"" % i[a].replace('"', '""') for a,_ in enumerate(i)])

else:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import cm

    fig = plt.figure(figsize=(8.5, 12))
    ax = fig.add_subplot(111)
    ax.grid(True, fillstyle='left')
    nf = len(leftvals)
    for font in leftvals:
        color = cm.jet(1.5*font/nf)
        ax.plot(leftvals[font], topvals[font], 'ro', color=color, marker=".")
        plt.figtext((font+1.)/(nf+1), 0.95, "font %d" % font, color=color)
    maxleft = (maxtop + 50) * 8.5 / 12
    plt.xticks(np.arange(0, maxleft, 50))
    plt.yticks(np.arange(0, maxtop + 50, 50))
    plt.xlim(0, maxleft)
    plt.ylim(0, maxtop + 50)
    plt.gca().invert_yaxis()
    fig.savefig("map.png")
    fig.clf()
    plt.close(fig)

