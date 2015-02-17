#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

csv = open(sys.argv[1], 'r').read()
csvtab = csv.split('\n')

circourante = " "
regexcirc = re.compile('.*(Circonscription : .* - [0-9]{1,2}(e|ère))</i>",".*')
regexdepu = re.compile('.*","(A|AR|AT|AD|R|HD|DD)"')
regexplafond = re.compile('.*"(Plafond.*)".*')
regexscrutin = re.compile('.*(Scrutin contesté|Scrutin non contesté).*')
regexcorrect = re.compile('.*(<i>(Département|Circonscription).*</i>).*')
scrutin = ""
plafond = ""
buffercirc = ""
buffercircline = ""
headers = '"Candidat", "Dépenses totales", "Recettes totales", "Dons", "Apports partis", "Concours en nature", "Autres", "Apports personnel", "Soldes compte de campagne", "Dév (1)", "RFE (2)", "Déc. CNCCFP", "Circoncription", "Plafond de dépenses", "Scrutin"\n'

for i in range(len(csvtab)-1):
	if regexcirc.match(csvtab[i]):
		circourante = regexcirc.match(csvtab[i]).group(1).split(' : ')[1].replace('</i>', '')
	if regexplafond.match(csvtab[i]):
		plafond = regexplafond.match(csvtab[i]).group(1)
		plafond = plafond.split('"')[0].split(' : ')[1]
	if regexscrutin.match(csvtab[i]):
		scrutin = regexscrutin.match(csvtab[i]).group(1)
		scrutin = scrutin.replace('",""', '')
	if csvtab[i][len(csvtab[i])-1] != '"':
		csvtab[i+1] = csvtab[i] + '/' + csvtab[i+1]
		continue
	if regexdepu.match(csvtab[i]):
		buffercircline += csvtab[i][:-3] + ',"' + circourante + '","' + plafond + '","' + scrutin + '"\n' 
		if regexcorrect.match(buffercircline):
			buffercircline = regexcorrect.sub('', buffercircline)


	buffercirc += buffercircline
	buffercircline = ""
	
open('compte2012.csv', 'w').write(headers + buffercirc)