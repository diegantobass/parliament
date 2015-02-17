#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

csv = open(sys.argv[1], 'r').read()
csvtab = csv.split('\n')

circourante = ""
regexcirc = re.compile('(.*)<i>(Circoncription.*[0-9])</i>(.*)')
regexdepu = re.compile('.*","(A|AR|AT|AD|R|HD)"')
regexplafond = re.compile('.*"(Plafond.*)",,+')
regexrembours = re.compile('.*"(Rembours.*)",,+')
regexscrutin = re.compile('.*(Scrutin contesté|Scrutin non contesté).*')
correctnom = re.compile('"(M.*)",{11}')
scrutin = ""
nom = ""
plafond = ""
rembours = ""
buffercirc = ""
headers = '"Candidat", "Dépenses totales", "Recettes totales", "Dons", "Apports partis", "Concours en nature", "Autres", "Apports personnel", "Soldes compte de campagne", "Dév (1)", "RFE (2)", "Déc. CNCCFP", "Circoncription", "Plafond de dépenses", "Remboursement maximum", "Scrutin"\n'

for i in range(len(csvtab)-1):
	if "Circoncription" in csvtab[i]:
		matchedline = regexcirc.match(csvtab[i])
		circourante = matchedline.group(2).split(' : ')[1]
	if regexplafond.match(csvtab[i]):
		plafond = regexplafond.match(csvtab[i]).group(1)
		plafond = plafond.split('"')[0].split(' : ')[1]
	if regexrembours.match(csvtab[i]):
		rembours = regexrembours.match(csvtab[i]).group(1)
		rembours = rembours.replace('",,"', ' ').split(' : ')[1]
	if regexscrutin.match(csvtab[i]):
		scrutin = regexscrutin.match(csvtab[i]).group(1)
		scrutin = scrutin.replace('",""', '')
	if csvtab[i][len(csvtab[i])-1] != '"':
		csvtab[i+1] = csvtab[i] + '/' + csvtab[i+1]
		continue
	if regexdepu.match(csvtab[i]):
		if correctnom.match(csvtab[i-1]):
			csvtab[i] = csvtab[i].replace('",,,,,,,,,,,/"', '')
		buffercirc += csvtab[i] + ',"' + circourante + '","' + plafond + '","' + rembours + '","' + scrutin + '"\n' 

open('compte2007.csv', 'w').write(headers + buffercirc)