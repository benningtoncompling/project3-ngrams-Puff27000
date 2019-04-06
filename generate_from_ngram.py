#!/usr/bin/env python3

#generate_from_ngram.py
#author: Puff Marx
#created: 04/2019
#random sentence generator for any given authorial style based on output from build_ngram_model.py
import sys
import random
import time #from stack overflow
random.seed(time.time()) #from stack overflow

input_file = sys.argv[1]
output_file = sys.argv[2]


def create_ngram_dicts_from_file(input_file):
    curr_state = 0
    unigram_dict = {}
    bigram_dict = {}
    trigram_dict = {}
    with open(input_file, 'r') as file_to_read:
        for line in file_to_read.readlines(): #otherwise we'll go through character by character
            if "\\1-grams:" in line:
                curr_state = 1
            elif "\\2-grams:" in line:
                curr_state = 2
            elif "\\3-grams:" in line:
                curr_state = 3
            elif curr_state == 1: #create 1-grams dict
                no_newlines_line = line.replace("\n", "")
                unigram_line_list = no_newlines_line.split(" ")
                unigram_dict[unigram_line_list[3]] = unigram_line_list[1]

            elif curr_state == 2: #create 2-grams dict
                no_newlines_line = line.replace("\n", "")
                bigram_line_list = no_newlines_line.split(" ")
                if bigram_line_list[3] not in bigram_dict:
                    bigram_dict[bigram_line_list[3]] = {bigram_line_list[4]:bigram_line_list[1]}
                else:
                    bigram_dict[bigram_line_list[3]][bigram_line_list[4]] = bigram_line_list[1]

            elif curr_state == 3: #create 3-grams dict
                no_newlines_line = line.replace("\n", "")
                trigram_line_list = no_newlines_line.split(" ")
                first_phrase = trigram_line_list[3] + " " + trigram_line_list[4]
                if first_phrase not in trigram_dict:
                    trigram_dict[first_phrase] = {trigram_line_list[5]:trigram_line_list[1]}
                else:
                    trigram_dict[first_phrase][trigram_line_list[5]] = trigram_line_list[1]
    return unigram_dict, bigram_dict, trigram_dict


def generate_random_unigram_sentence(unigram_dict):
    random_sentence_list = []
    random_sentence_list.append("<s>") #start the sentence with the BOS tag
    while "</s>" not in random_sentence_list[-1]: #-1 checks the last element
        random_float = random.random()  # generates a random number between 0 and 1; purloined from the internet
        sum = 0.0
        for key, value in unigram_dict.items():
            sum += float(value)
            if sum > random_float:
                if key == "<s>":
                    break
                random_sentence_list.append(key)
                break

    random_sentence_string = " ".join(random_sentence_list) + "\n"
    return random_sentence_string

def generate_random_bigram_sentence(ngram_dict):
    random_sentence_list = ["<s>"]
    random_float = random.random()
    sum = 0.0
    for second_word in ngram_dict["<s>"]:
        probability = ngram_dict["<s>"][second_word]
        #print(probability)
        sum += float(probability)
        if sum > random_float:
            random_sentence_list.append(second_word)
            break
    while "</s>" not in random_sentence_list[-1]: #-1 checks the last element
        random_float = random.random()  # generates a random number between 0 and 1; purloined from the internet
        sum = 0.0
        prev_word = random_sentence_list[-1]
        for second_word in ngram_dict[prev_word]:
            probability = ngram_dict[prev_word][second_word]
            sum += float(probability)
            if sum > random_float:
                random_sentence_list.append(second_word)
                break

    random_sentence_string = " ".join(random_sentence_list) + "\n"
    #print(random_sentence_list)
    return random_sentence_string









#main
unigram_dict, bigram_dict, trigram_dict = create_ngram_dicts_from_file(input_file) #returning the three ngram dicts for use

generate_random_bigram_sentence(bigram_dict)
with open(output_file, 'w') as open_outfile:
    open_outfile.write("unigram-generated sentences: " + "\n")
    for i in range(0,5):
        open_outfile.write(generate_random_unigram_sentence(unigram_dict))
    open_outfile.write("bigram-generated sentences: " + "\n")
    for i in range(0,5):
        open_outfile.write(generate_random_bigram_sentence(bigram_dict))


    # look at all the n-grams starting with <s> or with the most recent word you generated

    #find the dict entry whose value is just above your random number

