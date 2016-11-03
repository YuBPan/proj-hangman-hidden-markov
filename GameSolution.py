import re
import operator
import collections

class GameSolution():

	max_num_words = 5		#[hard code!]
	max_num_sentences = 5	#[hard code!]

	dic_ngram_freq = {}
	defult_freq = 0.0
	guessed_letters = []
	word_dict = {}
	naive_guess = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']
	naive_guess_i = 0
	naive_guess_max_perventage = 0.4	#[hard code!]
	allow_guess = 0


	def __init__(self, allow_guess):
		total = self.get_word_count('w2_.txt')
		self.load_ngram_freq('w2_.txt', total)
		self.allow_guess = allow_guess
		return

	def init(self):
		self.guessed_letters = []
		self.naive_guess_i = 0

	def load_ngram_freq(self, fileName, total):
		# dic_ngram_freq = {}
		f = open(fileName, 'r')
		for line in f:
			splited = line.split()
			self.dic_ngram_freq[(splited[1], splited[2])] = float(splited[0]) / total
		# return dic_ngram_freq

	def get_word_count(self, fileName):
		# word_set = set()
		word1_set = set()
		word2_set = set()
		pair_count = 0
		total = 0
		f = open(fileName, 'r')	
		for line in f:
			pair_count += 1
			splited = line.split()
			total += int(splited[0])
			if not splited[1] in self.word_dict:
				self.word_dict[splited[1]] = 1
			else:
				self.word_dict[splited[1]] += 1
			if not splited[2] in self.word_dict:
				self.word_dict[splited[2]] = 1
			else:
				self.word_dict[splited[2]] += 1				
			word1_set.add(splited[1])
			word2_set.add(splited[2])
		self.defult_freq = 1.0 * 1 / pair_count
		return total


	def get_ngram_freq(self, word1, word2):
		# return 1.0
		if (word1, word2) in self.dic_ngram_freq:
			# print 'Found ngram freq for given pairs (%s, %s) = %.10f' % (word1, word2, self.dic_ngram_freq[(word1, word2)])
			return self.dic_ngram_freq[(word1, word2)]
		else:
			# print 'No ngram freq for given pairs (%s, %s), use default = %.10f' % (word1, word2, self.defult_freq)
			return self.defult_freq
		
	# words, freq example
	# def get_top_words_freq(self, input_array):
	# 	return [[('have', 0.2), ('hate', 0.2), ('hair', 0.3)],
	# 			[('a', 0.2), ('access', 0.2)],
	# 			[('good', 0.1), ('tooo', 0.3), ('bady', 0.3)],
	# 			[('day', 0.1), ('daa', 0.2), ('dao', 0.3)]
	# 			]

	def get_top_words_freq_naive(self, input_array):
		splited = input_array.split()
		# print splited
		words_freq = []
		for i in range(0, len(splited)):
			filtered = self.get_top_words_freq_naive_helper(splited[i])
			# print filtered
			words_freq.append(filtered)
		# print 'words_freq', words_freq
		return words_freq

	def get_top_words_freq_naive_helper(self, input):
		regex = '^' + input.replace('_', '[a-z]') + '$'		# suppose no A-Z
		# print 'regex', regex
		filtered = []
		reobj = re.compile(regex)
		for key in self.word_dict.keys():
			if(reobj.match(key)):
				filtered.append((key, self.word_dict[key]))
		sorted_filtered = sorted(filtered,key=operator.itemgetter(1))
		# print sorted_filtered
		if len(sorted_filtered) == 0:
			print 'len(sorted_filtered) == 0'
			return []
		elif len(sorted_filtered) > self.max_num_words:
			return sorted_filtered[-1 * self.max_num_words:]
		else:
			return sorted_filtered


	def get_sentences_prob(self, input_array):
		# words_freq = self.get_top_words_freq(input_array)
		words_freq = self.get_top_words_freq_naive(input_array)
		# print 'words_freq', words_freq
		sentence = []
		prob = 1.0
		sentences_prob = []
		self.get_sentences_prob_helper(words_freq, 0, sentence, prob, sentences_prob)
		# print 'sentences_prob', len(sentences_prob), sentences_prob
		sorted_sentences_prob = sorted(sentences_prob, key=operator.itemgetter(1))
		# print 'sorted_sentences_prob', len(sorted_sentences_prob), sorted_sentences_prob
		if len(sorted_sentences_prob) > self.max_num_sentences:
			return words_freq, sorted_sentences_prob[-1 * self.max_num_sentences:]
		else:
			return words_freq, sorted_sentences_prob

	def get_sentences_prob_helper(self, words_freq, i, sentence, prob, sentences_prob):
		# print 'dfsing...'
		if i == len(words_freq):	# now save temp sentence and prob
			sentences_prob.append((list(sentence), prob))
			return 
		for j in range(0, len(words_freq[i])):
			prob_old = prob
			if len(sentence) != 0:
				prob *= self.get_ngram_freq(sentence[-1], words_freq[i][j][0]) *  words_freq[i][j][1]
			else:
				prob *= words_freq[i][j][1]
			sentence.append(words_freq[i][j][0])
			self.get_sentences_prob_helper(words_freq, i+1, sentence, prob, sentences_prob)
			
			prob = prob_old
			del sentence[-1]

	def get_most_letter(self, words_freq, sentences_prob):
		# print sentences_prob
		letter_dict = {}
		max_count = 0
		max_char = ''
		for sentence, prob in sentences_prob:				# loop each (sentence, prob)
			# print 'sentence', sentence
			# print 'prob', prob
			for i in range(0, len(sentence)):					# loop each word in sentence
				# if len(words_freq[i]) == 1:
					# continue
				for c in sentence[i]:
					if c in self.guessed_letters:
						continue
					if not c in letter_dict:
						letter_dict[c] = prob
					else:
						letter_dict[c] += prob
					if letter_dict[c] > max_count:
						max_count = letter_dict[c]
						max_char = c
		return max_char

	def get_guess_letter(self, input_array, remain_guess):
		letter = ''
		if float(self.allow_guess - remain_guess) / self.allow_guess < self.naive_guess_max_perventage and self.naive_guess_i < len(self.naive_guess):
			letter = self.naive_guess[self.naive_guess_i]
			self.naive_guess_i += 1
		else:
			words_freq, sentences_prob = self.get_sentences_prob(input_array)
			print 'sentences_prob', sentences_prob
			letter = self.get_most_letter(words_freq, sentences_prob)
			if letter == '' and self.naive_guess_i < len(self.naive_guess):
				letter = self.naive_guess[self.naive_guess_i]
				self.naive_guess_i += 1
		if letter != '':
			self.guessed_letters.append(letter)				
		return letter
	
if __name__ == "__main__":
	gameSolution = GameSolution()
	# gameSolution.guessed_letters = ['d', 'a']



