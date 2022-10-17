import sys, time

start_time = time.time()

#alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpha = "QXJZVFWBKGPMHDCYTLNUROISEA"
len_alpha = 26
full = 0b11111111111111111111111111

def toBin(word):
	r = 0
	found = 0
	for i in range(len_alpha):
		if alpha[i] in word:
			found += 1
			r += 2**i
			if found == 5:
				return r
	return 0

def fromBin(x):
	return word_dict[x]

def decode_pair(p):
	return pairsDict[p]

def isCollides(a, b):
	return (a & b) != 0

def FindMatch(pattern, pairs):
	missing = full ^ pattern
	#print(missing)
	for i in range(len_alpha):
		if (missing ^ 2**i) in pairs:
			return (missing ^ 2**i)
	return False

def prettify(words):
	r = []
	for w in words:
		r.append(fromBin(w))
	return ",".join(r)

if __name__ == "__main__":
	word_dict = {}
	words = set()
	with open(sys.argv[1], 'r') as f:
		raw_words = [line for line in f.read().splitlines()]
		for word in raw_words:
			k = toBin(word)
			words.add(k)
			word_dict[k] = word

	# Remove words that contain duplicate letters
	words = list(filter(lambda word: word != 0, words))
	# Find pairs
	pairs = set()
	pairsDict = {}
	for word1 in words:
		for word2 in words:
			if not isCollides(word1, word2):
				pairs.add(word1 | word2)
				pairsDict[word1 | word2] = (word1 , word2)
	results = set([])

	for pair1 in pairs:
		for word in words:
			if not isCollides(pair1, word):
				pattern = pair1 | word
				match = FindMatch(pattern, pairs)
				if match:
					p = [word, decode_pair(pair1), decode_pair(match)]
					result = [p[0], p[1][0], p[1][1], p[2][0], p[2][1]]
					result.sort()
					results.add(tuple(result))

	print("Done (in %s s)"%(time.time() - start_time))
	for result in results:
		print(prettify(result))