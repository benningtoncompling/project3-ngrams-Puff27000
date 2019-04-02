#!/usr/bin/env python3
#Computational Linguistics with Justin! Project 3
#Puff Marx
#03/2019

import sys
input_file = sys.argv[1]
output_file = sys.argv[2]

#    scraps        raw_text = open_in_file.read()
         #   marked_text = raw_text.replace("\n", " </s> \n")
         #   open_out_file.write(marked_text)
         #    iterator = iter(unigrams_list) #next couple of lines developed from an idea found on stack overflow
            #bigrams_list = zip(unigrams_list, unigrams_list)

#Take in an input file and output a file with the probabilities of each unigram, bigram, trigram of the input text
#make sure to add beginning/end of sentence markers

#adding sentence markers:

def add_sentence_markers():
    with open(input_file, 'r') as open_in_file:
        with open(output_file, 'w') as open_out_file:
            for line in open_in_file.readlines():
                marked_bos_line = "<s> " + line #+ "</s>" -- adding this puts the end of sentence marker after the newline. We don't want newline characters to be included in our n-grams.
                marked_bos_eos_line = marked_bos_line.replace("\n", " </s> ")
                open_out_file.write(marked_bos_eos_line.lower())
    return output_file


#getting a list of unigrams, split on whitespace

def get_unigrams(spaced_tagged_file):
    spaced_tagged_file = marked_text_file
    words_list = []
    with open(spaced_tagged_file, 'r') as open_in_file:
        for line in open_in_file.readlines():
            words_list += line.split(" ")
    return words_list

#make a list of bigrams from the unigram list
def get_bigrams(unigrams_list):
    bigrams_list = []
    for i in range(0, len(unigrams_list)-1):
        if unigrams_list[i] != "</s>":
            bigrams_list.append((unigrams_list[i], unigrams_list[i+1]))
    return(bigrams_list)

#make a list of trigrams from the unigram list-- ok? Or do I need it as a unigram and a bigram?
def get_trigrams(unigrams_list):
    trigrams_list = []
    for i in range(0, len(unigrams_list)-2):
        trigrams_list.append((unigrams_list[i], unigrams_list[i+1], unigrams_list[i+2]))
    return(trigrams_list)

#making a dictionary for counting unigrams
def generate_unigram_dict(unigram_list):
    unigram_dict = {}
    for unigram in unigram_list:
        if unigram not in unigram_dict:
            unigram_dict[unigram] = 1
        else:
            unigram_dict[unigram] += 1
    return unigram_dict

#making a dictionary for counting bigrams
def generate_bigram_dict(bigram_list):
    bigram_dict = {}
    for i,j in bigram_list:
        x = i.lower()
        y = j.lower()
        if x not in bigram_dict:
            bigram_dict[x] = {y:1}
        elif x in bigram_dict and y not in bigram_dict[x]:
            bigram_dict[x][y] = 1
        else:
            bigram_dict[x][y] += 1
    return(bigram_dict)

#making a dictionary for counting trigrams
def generate_trigram_dict(trigram_list):
    trigram_dict = {}


#get the probability of ONE unigram at a time
def get_unigram_probability(given_unigram, unigram_list, total_unigram_count): #we want the number of times our given unigram appears, divided by the number of unigrams total

    given_unigram_count = 0
    for unigram in unigram_list:

        if given_unigram == unigram:
            given_unigram_count += 1

    given_unigram_probability = given_unigram_count/total_unigram_count
    return given_unigram_probability

#get the probability of ONE bigram at a time
def get_bigram_probability(given_bigram, bigram_dict): #we want the count of how many times the given bigram appears, divided by the count of how many times the first word in the bigram appears

    first_word = given_bigram[0]
    first_word_count = 0
    for key, value in bigram_dict[first_word].items():
        first_word_count += value  #this should give how many times the first word appears-- our denominator.

    second_word = given_bigram[1]
    if second_word in bigram_dict[first_word].keys():

        bigram_occurrences = bigram_dict[first_word][second_word]
        bigram_probability = bigram_occurrences/first_word_count
        return bigram_probability

    else:
        print(first_word + " " + second_word + " : bigram not found")


#get the probability of ONE trigram at a time: need count of whole trigram divided by count of the bigram. ex) P(man| the old) = ct(the old man) / ct(the old)
def get_trigram_probability(given_trigram, trigram_dict):










#main-ish

#adding sentence markers
marked_text_file = add_sentence_markers()

#unigram counting
unigrams = get_unigrams(marked_text_file) #making a list of unigrams
unigram_count = len(unigrams) #checking how many total unigrams (not unique) from the list
print("unigram (token) count from list: " + str(unigram_count))
unigram_dict = generate_unigram_dict(unigrams)
print("unigram (token) count from dict (unique tokens): " + str(len(unigram_dict)))

print("unigram prob test: " + str(get_unigram_probability("is", unigrams, unigram_count))) #testing unigram probability calculator-- it works!


#bigram counting
bigrams = get_bigrams(unigrams)
bigram_count = len(bigrams)
print("bigram count from list: " + str(bigram_count))
bigram_dict = generate_bigram_dict(bigrams)
unique_bigram_counter = 0
for key in bigram_dict: #getting count of unique bigrams
    for values in bigram_dict[key]:
        unique_bigram_counter += 1
print("bigram count from dict (unique bigrams): " + str(unique_bigram_counter))

print("bigram prob test: " + str(get_bigram_probability(("of", "the"), bigram_dict))) #testing bigram probability calculator-- it works!



#trigram counting
trigrams = get_trigrams(unigrams)
trigram_count = len(trigrams)
print("trigram count: " + str(trigram_count))












