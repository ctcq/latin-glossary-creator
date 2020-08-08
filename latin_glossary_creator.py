import sys
import os
import re
import unidecode


#Returns number of occurences of a form of the given word until (and excluding) text 'num_text'
def getOccurencesUntil(word, num_text):
	if not type(word) == str:
		return "", -1
	if not type(num_text) == int:
		return "", -2
	if not num_text in range(1, len(texts_vocab)+1):
		return "", -3
	
	count = 0
	lections = []
	lection_counter = 1
	lemmatized = lemmatizer.lemmatize([word])[0][1]
	for t_dict in texts_vocab[:num_text]:
		if lemmatized in t_dict.keys():
			count += t_dict[lemmatized]
			lections.append(lection_counter)
		lection_counter += 1
		
	return lemmatized, count, lections

def generate_glossary():
	all_words = []
	for t_dict in texts_vocab:
		for w in t_dict:
			if not w in all_words:
				all_words.append(w)
	
	all_words = [w for w in all_words if re.fullmatch("[a-z]+", w)] #remove artifacts
	all_words.sort() #Sort alphabetically
	glossary = {}
	current_letter = all_words[0][0]
	glossary[current_letter] = []
	for word in all_words:
		if not word[0] == current_letter:
			current_letter = word[0]
			glossary[current_letter] = []
		glossary[current_letter].append((word , getOccurencesUntil(word, len(texts_vocab))[2])) #List with lections numbers a word occurs in
	
	return glossary
	
def glossar(outdir):
	string = ""
	glossary = generate_glossary()
	html = ""
	html_body = "<br><br>"
	for letter in glossary.keys():
		word_list = ""
		for word_tuple in glossary[letter]:
			word_list += f"<li><b>{word_tuple[0]}</b> : {word_tuple[1]}</li>"
		html_body += f"<h3 id='letter-{letter}'>{letter}</h3><ul>{word_list}</ul>"
	
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	index = ""
	for l in alphabet:
		index += f"<a href='#letter-{l}'>| {l} </a>"
	index_header = f"<div style='position:fixed; background-color:white; padding:10px; top:0;'>{index}</div>"
	
	html += f"<html><head></head><body>{index_header}{html_body}</body></html>"
	
	f = open(os.path.join(outdir, 'glossar.html'), 'w')
	f.write(html)
	f.close() 
	
	print(f"Wrote glossar to file {os.path.join(outdir, 'glossar.html')}.")
	return html
	
#Color formatting for the output
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def run():
	while(True):
		print("-------------------------------------------------\n")
		print(f"{color.BOLD}Neue Eingabe:{color.END}")
		word = input(f"Nach welcher {color.BOLD}Vokabel{color.END} soll gesucht werden? \n")
		num = input(f"Bis zu welcher {color.BOLD}Lektion{color.END} soll die Häufigkeit dieser Vokabel gezählt werden? \n")
		num = int(num)
		print("\n")
		result = getOccurencesUntil(word, num) #Assuming the first text corresponds to lektion 1
		print(f"{color.BOLD}Ergebnis:{color.END} \n")
		if result[1] == -1:
			print("Fehler in der Eingabe des Wortes...")
		elif result[1] == -2:
			print(f"{color.BOLD}Fehler in der Eingabe {color.END}: Die Nummer der Lektion muss eine Zahl sein...")
		elif result[1] == -3:
			print(f"{color.BOLD}Fehler in der Eingabe{color.END}: Die Nummer der Lektion darf {len(texts_vocab)} nicht übersteigen.")
		else:
			print(f"Bis zur {color.BOLD}Lektion {num+1}{color.END} \n kommt die Form {color.BOLD}{result[0]}{color.END} \n zum Wort {color.BOLD}{word}{color.END} \n insgesamt an {color.BOLD + color.UNDERLINE}{result[1]}{color.END + color.END} verschiedenen Stellen vor.\n")
			print(f"Die Vokabel kommt in den folgenden Lektionen vor: {result[2]}")

def start():
	run()


#First console argument is folder with text in alphbetical order
file_directory = sys.argv[1]

#Import cltk modules and initiate objects...
from cltk.corpus.utils.importer import CorpusImporter
corpus_importer = CorpusImporter("latin")

print("Importing latin models corpus. This may take a while...")
corpus_importer.import_corpus("latin_models_cltk")

from cltk.lemmatize.latin.backoff import BackoffLatinLemmatizer
lemmatizer = BackoffLatinLemmatizer()

print("Initiated cltk model. Loading files from {file_directory}...")

files = [os.path.join(file_directory, f) for f in os.listdir(file_directory) if os.path.isfile(os.path.join(file_directory, f))]
files.sort(key=lambda x : int(x.split("_")[-1].split(".")[0]))

texts_vocab = [] #List storing information about each word

for f in files:
	#Read file contents
	fr = open(f, 'r')
	string = fr.read()
	fr.close()
	
	#Remove every character except letters
	string = unidecode.unidecode(string) #Remove accents
	string = string.lower()
	string = string.replace("\t", " ")
	string = string.replace("\n", " ")
	string = re.sub("[^a-z]", " ", string)
	#List containing each word of the text
	string = re.sub("[ ]+", " ", string)
	words = string.split(" ")	
	
	text_dict = {} #Dict storing amount of occurences for each word in this text

	lemmatized = lemmatizer.lemmatize(words) #Contains words of the text in a generals form (Stammform)

	for word in lemmatized:
		if word[1] in text_dict.keys():
			text_dict[word[1]] += 1
		else:
			text_dict[word[1]] = 1
			
	texts_vocab.append(text_dict)

if len(sys.argv) > 2:
	glossar(sys.argv[2])
else:
	run()
