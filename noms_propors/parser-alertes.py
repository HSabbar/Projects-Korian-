import re

namefile = "Transmissions120SurvivantsPlusenDecembre2014AlerteSelles0.txt"
file = open("data/"+namefile, 'r',  encoding ='ISO-8859-1')

f = open("data-anno/"+namefile, "w")

pattern_cible = re.compile(r'Pour(.*?)Raison')
pattern_cible_s = re.compile(r'(\(par(.*?\)))')


for line in file:
	find = re.search(pattern_cible, line).group(1)
	find_s = re.findall(pattern_cible_s, line)
	if find:
		# print(find)
		line = re.sub(find, " XXXXXX ", line)
	else:
		break

	for x in find_s:
		# print(x[0])
		line = re.sub(x[0], '', line)

	line += "signer par " + str(len(find_s)) + " aide soignantes \n"
	f.write(line)

f.close()


