#!/usr/bin/env python3
#Computational Linguistics with Justin! Project 3
#Puff Marx
#03/2019


import sys
import math
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

def add_sentence_markers(input_file):
    output_list = []
    with open(input_file, 'r') as open_in_file:
        for line in open_in_file.readlines():
            marked_bos_line = "<s> " + line #+ "</s>" -- adding this puts the end of sentence marker after the newline. We don't want newline characters to be included in our n-grams.
            marked_bos_eos_line = marked_bos_line.replace("\n", " </s>")
            output_list.append(marked_bos_eos_line.lower())
    return output_list #list of sentences


#getting a list of unigrams, split on whitespace

def get_unigrams(input_file):
    spaced_tagged_sentences = add_sentence_markers(input_file)
    print(spaced_tagged_sentences[:1])
    words_list = []

    for line in spaced_tagged_sentences:
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
        if unigrams_list[i] != "</s>" and unigrams_list[i+1] != "</s>":
            trigrams_list.append((unigrams_list[i] + " " + unigrams_list[i+1], unigrams_list[i+2])) #you can do str ops inside append!!
    print(trigrams_list[25:30]) #test
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
def generate_bigram_dict(bigram_list): #can use this for trigrams too
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
def get_unigram_probability(given_unigram, unigram_dict, unigram_list): #we want the number of times our given unigram appears, divided by the number of unigrams total

    given_unigram_probability = unigram_dict[given_unigram]/len(unigram_list)
    return given_unigram_probability

#get the probability of ONE bigram at a time
def get_bigram_probability(given_bigram, bigram_dict, unigram_dict): #we want the count of how many times the given bigram appears, divided by the count of how many times the first word in the bigram appears

    first_word = given_bigram[0]
    first_word_count = unigram_dict[first_word]  #this should give how many times the first word appears-- our denominator.

    second_word = given_bigram[1]
    if second_word in bigram_dict[first_word]:

        bigram_occurrences = bigram_dict[first_word][second_word]
        bigram_probability = bigram_occurrences/first_word_count
        return bigram_probability

    else:
        print(first_word + " " + second_word + " : bigram not found")


#get the probability of ONE trigram at a time: need count of whole trigram divided by count of the bigram. ex) P(man| the old) = ct(the old man) / ct(the old)
def get_trigram_probability(given_trigram, trigram_dict, bigram_dict):

    first_phrase = given_trigram[0] #the old
    split_phrase = given_trigram[0].split(" ")
    first_tuple_count = bigram_dict[split_phrase[0]][split_phrase[1]]

    second_word = given_trigram[1]
    if second_word in trigram_dict[first_phrase]:

        trigram_occurrences = trigram_dict[first_phrase][second_word]
        trigram_probability = trigram_occurrences/first_tuple_count
        return trigram_probability











#main-ish function testing




#unigram counting
unigrams = get_unigrams(input_file) #making a list of unigrams and adding sentence markers
unigram_count = str(len(unigrams)) #checking how many total unigrams (not unique) from the list
print("unigram (token) count from list: " + unigram_count)
unigram_dict = generate_unigram_dict(unigrams)
unique_unigrams = str(len(unigram_dict))
print("unigram (token) count from dict (unique tokens): " + unique_unigrams)
print("unigram prob test: " + str(get_unigram_probability("is", unigram_dict, unigrams))) #testing unigram probability calculator-- it works!


#bigram counting
bigrams = get_bigrams(unigrams)
bigram_count = str(len(bigrams))
print("bigram count from list: " + bigram_count)
bigram_dict = generate_bigram_dict(bigrams)
unique_bigram_counter = 0
for key in bigram_dict: #getting count of unique bigrams
    for values in bigram_dict[key]:
        unique_bigram_counter += 1
unique_bigrams = str(unique_bigram_counter)

print("bigram count from dict (unique bigrams): " + str(unique_bigram_counter))

print("bigram prob test: " + str(get_bigram_probability(("of", "the"), bigram_dict, unigram_dict))) #testing bigram probability calculator-- it works!

#trigram counting
trigrams = get_trigrams(unigrams)
trigram_count = str(len(trigrams))
print("trigram count (non unique): " + trigram_count)
trigram_dict = generate_bigram_dict(trigrams)
unique_trigram_counter = 0 #should really make this a function
for key in trigram_dict:
    for values in trigram_dict[key]:
        unique_trigram_counter += 1
unique_trigrams = str(unique_trigram_counter)
print("trigram count from dict (unique trigrams): " + str(unique_trigram_counter))


#ACTUAL MAIN?


with open(output_file, 'w') as open_out_file:
    open_out_file.write("\data\\\n")
    open_out_file.write("ngram 1: type=" + unique_unigrams + " token=" + unigram_count + "\n")
    open_out_file.write("ngram 2: type=" + unique_bigrams + " token=" + bigram_count + "\n")
    open_out_file.write("ngram 3: type=" + unique_trigrams + " token=" + trigram_count + "\n")

    unigram_data_list = []
    open_out_file.write("\\1-grams: \n")
    for unigram in unigram_dict: #could sort this by count, referencing project 1 for syntax
        unigram_data_list.append(str(unigram_dict[unigram]) + " " + str(get_unigram_probability(unigram, unigram_dict, unigrams)) + " " + str(math.log10(get_unigram_probability(unigram, unigram_dict, unigrams))) + " " + unigram)
    open_out_file.write("\n".join(unigram_data_list)) #Justin's preference for adding \n

    bigram_data_list = []
    open_out_file.write("\\2-grams: \n")
    for first_word in bigram_dict: #could sort this by count, referencing project 1 for syntax
        for second_word in bigram_dict[first_word]:
            bigram_data_list.append(str(bigram_dict[first_word][second_word]) + " " + str(get_bigram_probability((first_word, second_word), bigram_dict, unigram_dict)) + " " + str(math.log10(get_bigram_probability((first_word, second_word), bigram_dict, unigram_dict))) + " " + str(first_word + " " + second_word))
    open_out_file.write("\n".join(bigram_data_list)) #Justin's preference for adding \n

    trigram_data_list = []
    open_out_file.write("\\3-grams: \n")
    for first_phrase in trigram_dict: #could sort this by count, referencing project 1 for syntax
        for second_word in trigram_dict[first_phrase]:
            trigram_data_list.append(str(trigram_dict[first_phrase][second_word]) + " " + str(get_trigram_probability((first_phrase, second_word), trigram_dict, bigram_dict)) + " " + str(math.log10(get_trigram_probability((first_phrase, second_word), trigram_dict, bigram_dict))) + " " + str(first_phrase + " " + second_word))
    open_out_file.write("\n".join(trigram_data_list)) #Justin's preference for adding \n







