from __future__ import division
import json
import re
import math
from collections import Counter
import heapq
import numpy as np 
from nlp import final_corpus
import time
import pickle
from pattern.en import suggest

def word_to_ngram_vector(word, n = 2):
	length = len(word)
	letters = [word[i:i+n] for i in range(length-n+1)]
	#print letters
	return Counter(letters)

def text_to_vector(text):
    word = re.compile(r'\w+')
    words = word.findall(text)
    #print Counter(words)
    return Counter(words)

def word_to_vector(word):
	letters = list(word)
	# print Counter(letters)
	return Counter(letters)


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def get_result(content_a, content_b):
    text1 = content_a
    text2 = content_b

    vector1 = word_to_ngram_vector(text1)
    vector2 = word_to_ngram_vector(text2)

    cosine_result = get_cosine(vector1, vector2)
    return cosine_result


def jaccard(a,b):
    a=list(a)
    b=list(b)
    union = list(set(a+b))
    intersection = list(set(a) - (set(a)-set(b)))
    # print "Union - %s" % union
    # print "Intersection - %s" % intersection
    jaccard_coeff = float(len(intersection))/len(union)
    # print "Jaccard Coefficient is = %f " % jaccard_coeff
    return jaccard_coeff

def open_buckets():
	filepath = './nlp/buckets_3.txt'
	buckets = []
	with open(filepath) as fp:  
	   line = fp.readline()
	   while line:
	       buckets.append(line.strip())
	       line = fp.readline()
	# print(buckets)
	return buckets

def create_bucket_candidates(buckets):
	candidates = []
	for line in buckets:
	       cur_list = line.strip()
	       cur_list = cur_list.rstrip(']')
	       cur_list = cur_list.lstrip('[')
	       cur_list = cur_list.split(',')

	       cur_candi = cur_list[0]
	       cur_candi = cur_candi.lstrip('\'')
	       cur_candi = cur_candi.lstrip('"')
	       cur_candi = cur_candi.rstrip('\'')
	       cur_candi = cur_candi.rstrip('"')

	       candidates.append(cur_candi)

	# print(candidates)
	return candidates


def find_similar_1(word,buckets,bucket_candidates):
	
	candidates = []
	distances = []
	
	start_time = time.clock()
	# count = 0
	for cur_candi in bucket_candidates:
		cur_candi_distance = get_result(cur_candi,word)
		distances.append(cur_candi_distance)
		


	end_time  = time.clock()
	# print(count)
	# print("*****************************************")
	# print("time to read = ", end_time-start_time)
	# print(len(buckets))
	# print(candidates)
	# print(distances)
	# print(distances)

	distances = np.array(distances)
	ind = np.argpartition(distances, -20)[-20:]
	# print(ind)

	closest_words = []
	distances_1 = []

	for i in ind:
		# print(candidates[i])
		# print(buckets[i])
		# print("*********************************")
		cur_bucket = buckets[i]
		cur_bucket = cur_bucket.rstrip(']')
		cur_bucket = cur_bucket.lstrip('[')
		cur_bucket = cur_bucket.split(',')

		# print(cur_bucket)
		# print("##################################")

		for j in range(len(cur_bucket)):
			cur_word = cur_bucket[j]
			cur_word = cur_word.rstrip('\'') 
			cur_word = cur_word.lstrip('\'') 
			closest_words.append(cur_bucket[j])
			distances_1.append(get_result(cur_bucket[j],word))

	# print("*****************************************")
	distances_1 = np.array(distances_1)
	ind = np.argpartition(distances_1, -10)[-10:]
	# print(ind)
	# print(closest_words)

	final_candidates = []
	for i in ind:
		# print(closest_words[i])
		final_candidates.append(closest_words[i])
	return final_candidates

def find_best_match(candidates ,word):
	"Most probable spelling correction for word."
	max = -1.0
	res = ""
	
	for c in candidates:
		if c!=word:
			if jaccard(c, word) > max:
				max = jaccard(c, word)
				res = c
	if (jaccard(res,word) + get_result(res,word))/2.0 > 0.63:
		return res
	else:
		return word

def get_english_suggestions(word):
	suggestions = []
	for cur in suggest(word):
		cur_word = cur[0]
		if(cur[1]!=0):
			suggestions.append(cur_word)

	if(len(suggestions) < 5):
		return suggestions
	else:
		return suggestions[0:5]

def read_json(data):
	text_detected = data["TextDetections"]
	meta_data = data["ResponseMetadata"]
	return text_detected , meta_data


def correct_text(text , meta_data):
	buckets = open_buckets()
	print("buckets opened")
	bucket_candidates = create_bucket_candidates(buckets)
	print("candidates created for buckets")
	print("chekcing words .... ")

	counter = 0

	for i in range(len(text)):
		counter+=1
		cur_text = text[i]["DetectedText"]
		words = cur_text.split()
		# print(words)
		for pos, word in enumerate(words):
			candidates_3 = get_english_suggestions(word)
			candidates_2 = list(final_corpus.candidates(word))
			corrected_word_candidates_2 = find_best_match(set(candidates_2+candidates_3),word)
			if  corrected_word_candidates_2 != word:
				corrected_word = corrected_word_candidates_2
				# print("1")
			else:
				candidates_1 = find_similar_1(word,buckets,bucket_candidates)
				total_candidates = set(candidates_1+candidates_2+candidates_3)
				corrected_word = find_best_match(total_candidates,word)
				# print("2")

			words[pos] = corrected_word

		text[i]["DetectedText"] = " ".join(words) 
		print(counter/len(text)*100)
		# print(words)
		# print("**********")
	json_dict = {}
	json_dict["TextDetections"] = text
	json_dict["ResponseMetadata"] = meta_data
	return json_dict


def main(aws_result):
	# input_path = "./out.txt"
	# output_path = "./corrected_out.txt"
	text_detected , meta_data = read_json(aws_result)
	return json.dumps(correct_text(text_detected, meta_data))

