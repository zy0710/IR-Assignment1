import numpy as np

#Question-d

#build the co-occurance dictionary and margin dictionary

N = 0
pair_dictionary = dict()
margin_dictionary = dict()
vac_set = list()

with open('data.txt','r') as file_in:
	lines = file_in.readlines()
	N = len(lines)
	for line in lines:
		words = line.split('\n')[0].split()
		words_set = list(set(words))
		for word in words:
			if word not in vac_set:
				vac_set.append(word)
		for word in words_set:
			if word not in margin_dictionary:
				margin_dictionary[word] = 0
			margin_dictionary[word] += 1

for i in range(len(vac_set)-1):
	for j in range(i+1, len(vac_set)):
		pair_dictionary[(vac_set[i], vac_set[j])] = 0

#count the co-occurance for each pair
with open('data.txt','r') as file_in:
	lines = file_in.readlines()
	for line in lines:
		words = line.split('\n')[0].split()
		words = list(set(words))
		for i in range(len(words)-1):
			for j in range(i+1,len(words)):
				if words[i] == words[j]:
					continue
				if(words[i],words[j]) in pair_dictionary:
					pair_dictionary[(words[i], words[j])] +=1
				else:
					pair_dictionary[words[j], words[i]] +=1

print('\n')

L = sorted(pair_dictionary.items(), key = lambda item:item[1], reverse=True)
print("For Question-d, the largest 10 counts are:")
for i in range(10):
	print(L[i])

print('\n\n')


#Question-e

def calculate_MI(pair_dictionary, margin_dictionary, variable_A, variable_B, N):
	'''
	:param pair_dictionary: pair co-occurance dictionary
	:param variable_A: name of variable x
	:param variable_B: name of variable y
	:param N: the total number of documents
	:return: A mutual information dicttionary for pair_dictionary
	'''

	N_A = margin_dictionary[variable_A]
	N_B = margin_dictionary[variable_B]
	N_AB = pair_dictionary[(variable_A, variable_B)]

	try:
		MI = (N_AB + 0.25) / (1 + N) * np.log2((N_AB + 0.25) * (N+1) / ((N_A + 0.5) * (N_B + 0.5)))\
			+ (N_A - N_AB + 0.25) / (N+1) * np.log2((N_A - N_AB + 0.25) * (N+1)/((N_A + 0.5) * (N-N_B+0.5)))\
			+ (N_B - N_AB + 0.25) / (N+1) * np.log2((N_B - N_AB + 0.25) * (N+1)/((N-N_A+0.5) * (N_B+0.5)))\
			+ (N - N_A - N_B + N_AB + 0.25) / (N+1) * np.log2((N - N_A - N_B + N_AB + 0.25) * (N+1) / ((N-N_A+0.5) * (N-N_B+0.5)))
	except:
		print('N_A, N_B, N_AB:',  N_A, N_B,N_AB)

	return MI

#calculate the Mutual Information

MI_dic = dict()
for variable_A, variable_B in pair_dictionary:
	MI_dic[(variable_A, variable_B)] = calculate_MI(pair_dictionary, margin_dictionary, variable_A, variable_B, N)

L = sorted(MI_dic.items(), key = lambda item:item[1], reverse=True)

print('For Question-e(1), the top 10 MI pairs are:')

for i in range(10):
	print(L[i])

print('\n\n')

print('For Question-e(2), the top 5 words which have the highest MI with <programming> in the collection')

count = 0
for pair in L:
	if 'programming' in pair[0]:
		print(pair)
		count += 1
	if count == 5:
		break