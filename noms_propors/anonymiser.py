import re


namefile = "Transmissions1815SurvivantsPlusenDecembre2014AlerteSelles0.txt"

file = open("data/"+namefile, 'r',  encoding ='ISO-8859-1')

pattern_barasite = r'|ã|ª|©|§|¨|´|\+|(|)|=|:|;|\.|,|\'|;|<|>|"'
pattern2 = r"|etait|refuse|mange|accept|sonne|avait|prend|occupe|après|celle|reste|signal|elle|"
patternum = r"^\d+\s|\s\d+\s|\s\d+$"

pattern_cible = re.compile(r"(\bmme\b|\bmadame\b|\bmr\b|\bmonsieur\b|\bm\b) (\w+)")

f = open("data-anno/"+namefile, "w")



for line in file:

	line = re.sub(pattern_barasite, '', line.lower())
	Ltxt = re.sub(pattern2, '', str(line))
	Ltxt = re.sub(patternum, '', str(Ltxt))
	Ltxt = re.sub(r'[^\w]', ' ', Ltxt)
	# print(line)
	if pattern_cible.findall(Ltxt):
		list_nomes = pattern_cible.findall(Ltxt)
		cible = list_nomes[0][1]

		if len(cible) == 1 or len(cible) > 4 :
			words = Ltxt.split()
			
			try:
				phrase = words[words.index(cible)-1:words.index(cible)+2]
				phrase = " ".join(phrase)

				if len(pattern_cible.findall(phrase)) > 0 :
					phrase_new = re.sub(r"\b"+cible+r"\b", "XXXXX", phrase)

				line = re.sub(phrase, phrase_new, Ltxt)

			except ValueError:
				pass

			

	
	f.write(line)

f.close()


