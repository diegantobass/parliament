#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

csv = open(sys.argv[1], 'r').read()
csvtab = csv.split('\n')

circourante = ""
regexcirc = re.compile('(.*)<i>(Circoncription.*[0-9])</i>(.*)')
regexdepu = re.compile('.*","[A|AR|AT|AD|R|HD]"')
regexplafond = re.compile('"(Plafond.*)",,+')
plafond = ""
regexrembours = re.compile('"(Rembours.*)",,+')
rembours = ""
buffercirc = ""
headers = '"Candidat", "Dépenses totales", "Recettes totales", "Dons", "Apports partis", "Concours en nature", "Autres", "Apports personnel", "Soldes compte de campagne", "Dév (1)", "RFE (2)", "Déc. CNCCFP", "Circoncription", "Plafond de dépenses", "Remboursement maximum"\n'

for i in range(len(csvtab)-1):
	if "Circoncription" in csvtab[i+1]:
		matchedline = regexcirc.match(csvtab[i+1])
		circourante = matchedline.group(2).split(' : ')[1]
	if regexdepu.match(csvtab[i]):
		buffercirc += csvtab[i] + ',"' + circourante + '","' + plafond + '","' + rembours + '"\n' 
	if regexplafond.match(csvtab[i]):
		plafond = regexplafond.match(csvtab[i]).group(1)
		plafond = plafond.replace('","', ' ').split(' : ')[1]
	if regexrembours.match(csvtab[i]):
		rembours = regexrembours.match(csvtab[i]).group(1)
		rembours = rembours.replace('",,"', ' ').split(' : ')[1]

open('compte2007.csv', 'w').write(headers + buffercirc)