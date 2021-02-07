"""
	This model is trained using Markov Chaning rule
 
	Default dataset is the script from the Game of throne.
"""


from nltk import WhitespaceTokenizer
import nltk
import random

STOP_WORD = ['.', '?', '!']

file = open("corpus.txt", 'r', encoding='utf-8')

wst = WhitespaceTokenizer()
token_sen = wst.tokenize_sents(file)
token = [word for sen in token_sen for word in sen]


"""
	Traning the model using bigrams.
	Bigrams are not very accurate but we can at least try for the input.
"""
def pre_bigram() -> dict:
	brg: dict = list(nltk.bigrams(token))

	bigrams = {}
	for head, tail in brg:
		bigrams.setdefault(head, {})
		bigrams[head].setdefault(tail, 0)

		bigrams[head][tail] += 1
	
	return bigrams


"""
	Traning the model using trigram.
	Trigram are most of the time accurate, but this can also fail sometime.
"""
def pre_trigram() -> dict:
	trg: dict = nltk.trigrams(token)

	trigrams: dict = {}

	for head1, head2, tail in trg:
		head = head1 + " " + head2

		trigrams.setdefault(head, {})
		trigrams[head].setdefault(tail, 0)

		trigrams[head][tail] += 1

	return trigrams



"""
	This function tries to predict the next based on the
 	pervious word using pre_bigram function returned dictionary.
	
	This function generate full sentence
"""
def bigram(bigrams: dict ,start: str) -> None:
	sentence = [start]

	while True:
		tails: dict = bigrams[start]
		tails_key = [x for x in tails.keys()]
		tails_value = [x for x in tails.values()]

		choice: str = random.choices(tails_key, tails_value)[0]
		sentence.append(choice)

		if len(sentence) > 4 and choice[-1] in STOP_WORD:
			break
	
	print(" ".join(sentence))



"""
	This function tries to predict the next based on the
 	pervious word using pre_trigram function returned dictionary.
	
	This function generate full sentence
"""
def trigram(trigrams: dict, start: str) -> None:
	sentence = [start]

	while True:
		tails: dict = trigrams[start]
		tails_key = [x for x in tails.keys()]
		tails_value = [x for x in tails.values()]

		choice: str = random.choices(tails_key, tails_value)[0]
		sentence.append(choice)

		start: str = start.split()[1] + " " + choice

		if len(sentence) > 3 and choice[-1] in STOP_WORD:
			break

	print(' '.join(sentence))

bigrams = pre_bigram()
trigrams = pre_trigram()

while True:
	word = input("Enter one or two word/s: ")

	try:
		if word == 'exit':
			break
		elif len(word.split()) == 1:
			bigram(bigrams, word)
		else:
			trigram(trigrams, word)
	except KeyError:
		print("Not Available")
