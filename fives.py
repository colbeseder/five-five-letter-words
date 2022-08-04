import sys, time

start_time = time.time()

def isCollides(group, word):
	return len(set(group + word)) != (len(group) + len(word))

def isNoDupes(word):
	return len(set(word)) == len(word)

def FindMatch(pattern, wordDict):
	alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	missing = []
	for c in alpha:
		if c not in pattern:
			missing.append(c)
	for i in range(len(missing)):
		key = ''.join(missing[:i] + missing[i+1:])
		#print(key)
		isMatch = key in wordDict
		if isMatch:
			return wordDict[key]
	return False

if __name__ == "__main__":
	with open(sys.argv[1], 'r') as f:
		words = [line for line in f.read().splitlines()]

	# Remove words that contain duplicate letters
	words = list(filter(lambda word: isNoDupes(word), words))

	wordDict = {}
	for word in words:
		wordDict["".join(sorted(word))] = word

	# Find pairs
	pairs = []
	for word1 in words:
		for word2 in words:
			if not isCollides(word1, word2):
				pairs.append(word1 + word2)

	pairsDict = {}
	for pair in pairs:
		pairsDict["".join(sorted(pair))] = pair

	print("Preparation done (%s s). Starting search"%(time.time() - start_time))

	start_time = time.time()

	for pair1 in pairs:
		for word in words:
			if not isCollides(pair1, word):
				pattern = pair1 + word
				match = FindMatch(pattern, pairsDict)
				if match:
					p = pattern + match
					prep = ",".join([p[i:i+5] for i in range(0, len(p), 5)])
					print("Found: %s (in %s s)"%(prep, int(time.time() - start_time)))
					exit

	print("Done (in %s s)"%(time.time() - start_time))
