import csv
import re
from typing import Pattern

path = "data/_57793TransmissionsSurvivors_2014V1.csv"

PATTERN_SUPP_HTML : Pattern = re.compile(r'<(.*?)>')

PATTERN_ASH : Pattern = re.compile(r'\bash\b|\bagent de service hôtelier\b|\bagent de service hotelier\b')
freq_ash = 0

PATTERN_AIDE_SOIGNANT : Pattern = re.compile(r'\bas\b|\bas\.\b|\baide-soignant\b|\baide soignant\b')
freq_as = 0

PATTERN_IDE : Pattern = re.compile(r'\bide\b')
freq_ide = 0

PATTERN_IDEC : Pattern = re.compile(r'\bchange\b')
freq_idec = 0

# /^((?!\bmedecin-co\b).)*$/|/^((?!\bmedco\b).)*$/| .*médecin(?=creek).*|
PATTERN_MEDECIN : Pattern = re.compile(r'\bmt\b|\bmt\.\b|\bdr\b|\bdr\.\b|\b(m(é|e)decin)?(?!-co)\b|\bdocteur\b')
freq_medecin = 0

f = open("data/_57793TransmissionsSurvivors_2014V1.txt", "a")


with open(path, 'r') as csvfile:
	for id_resident, id_etablissement, date_T, descrip in  csv.reader(csvfile, delimiter=';'):
		descrip = descrip.lower()

		descrip = re.sub(r'\bagrave\b', 'a', descrip)
		descrip = re.sub(r'\beacut\b|\begrave\b|\bpreacute\b', 'e', descrip)

		sub_html = re.findall(PATTERN_SUPP_HTML, descrip)
		for html in sub_html:
			if html:
				descrip = re.sub(r'\s+', ' ', descrip)
				descrip = descrip.replace(html, '')
				descrip = descrip.replace('<>', '')
				


		_ash = PATTERN_ASH.findall(descrip)
		if _ash :
			freq_ash += len(_ash)
		
		_as = PATTERN_AIDE_SOIGNANT.findall(descrip)
		if _as :
			freq_as += len(_as)

		_ide = PATTERN_IDE.findall(descrip)
		if _ide :
			freq_ide += len(_ide)

		_idec = PATTERN_IDEC.findall(descrip)
		if _idec :
			print(descrip)
			freq_idec += len(_idec)

		_medecin = PATTERN_MEDECIN.findall(descrip)
		# print(_medecin)
		for x, y in _medecin:
			if len(x) :
				# print(x)
				freq_medecin += 1
			

		f.write(descrip + '\n')
		# print(descrip)
		# break
f.close()
print('Agent de service hotelier : ' + str(freq_ash))
print('Aide soignant : ' + str(freq_as))
print('IDE : ' + str(freq_ide))
print('IDEC : ' + str(freq_idec))
print('Medecin : ' + str(freq_medecin))


s = 'c est medecin-co medecin-co mt mt. dr medecin-co plainte  médecin to respirer et réclame un medecin.<><>durrieu'
d = 'alerte eva (douleur): 5- le 13/12/2014 agrave; 10h00- pour lagnes robert lucien prosperraison : valeur eacute;leveacute;e ( 5).'

# print(re.sub('agrave', 'XXXX', d))

# find = PATTERN_MEDECIN.findall(s)
# print(find)

# for x, y in find:
# 	if len(x) :
# 		print(x)


