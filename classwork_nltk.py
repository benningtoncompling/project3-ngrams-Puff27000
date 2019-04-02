#!/usr/bin/env python3
import nltk
#nltk.download()

words = nltk.corpus.gutenberg.words("shakespeare-macbeth.txt")
#print(words[:20])
bigrams = list(nltk.bigrams(words))
#print(bigrams[:5])
total_words_in_book = len(words)
number_of_he = 0
for word in words:
    if word == 'he' or word == 'He':
        number_of_he += 1
#print(number_of_he)


def generate_bigrams():
    bigram_dict = {}
    for i,j in bigrams:
        x = i.lower()
        y = j.lower()
        if x not in bigram_dict:
            bigram_dict[x] = {y:1}
        elif x in bigram_dict and y not in bigram_dict[x]:
            bigram_dict[x][y] = 1
        else:
            bigram_dict[x][y] += 1

    print(bigram_dict)
    return(bigram_dict)

macbeth_bigram_dict = generate_bigrams()


def count_phrase_probability(first_word, second_word, bigram_dict):
    first_word_occurrences = 0
    first_word_probability = 0
    bigram_occurrences: int = 0

    if first_word in bigram_dict:
        for key, value in bigram_dict[first_word].items():
            first_word_occurrences += value
        first_word_probability = float(first_word_occurrences/total_words_in_book)
    #print("the probability of " + first_word + " : " + str(first_word_probability))
    if second_word in bigram_dict[first_word].keys():
            bigram_occurrences = bigram_dict[first_word][second_word]
    else:
        print(first_word + " " + second_word + " : bigram not found")
    bigram_probability = bigram_occurrences/first_word_occurrences
    #print("bigram occurs:" + str(bigram_occurrences))
    #print("first word occurs:" + str(first_word_probability))
    #print("the probability of " + first_word + " " + second_word + " : " + str(bigram_probability))
    #number of times he is appears divided by the number of times he appears
    return bigram_probability

#could have made a loop to run this function on any string... instead I called it lots of times by hand

#he is
print("<he is> : " + str(count_phrase_probability("he","is",macbeth_bigram_dict)))
print("<she is> : " + str(count_phrase_probability("she","is",macbeth_bigram_dict)))
print("<she ate> : " + str(count_phrase_probability("she","ate",macbeth_bigram_dict)))

#it was
it_was = count_phrase_probability("it","was", macbeth_bigram_dict)
was_a = count_phrase_probability("was", "a", macbeth_bigram_dict)
a_little = count_phrase_probability("a", "little", macbeth_bigram_dict)
little_thing = count_phrase_probability("little", "thing", macbeth_bigram_dict)
print("<it was a little thing> : " + str(it_was*was_a*a_little*little_thing))

#the earth trembled
the_earth = count_phrase_probability("the", "earth", macbeth_bigram_dict)
earth_trembled = count_phrase_probability("earth", "trembled", macbeth_bigram_dict)
print("<the earth trembled> : " + str(the_earth*earth_trembled))

#the night was quiet
the_night = count_phrase_probability("the", "night", macbeth_bigram_dict)
night_was = count_phrase_probability("night", "was", macbeth_bigram_dict)
was_quiet = count_phrase_probability("was", "quiet", macbeth_bigram_dict)
print("<the night was quiet> : " + str(the_night*night_was*was_quiet))

#a man appeared
a_man = count_phrase_probability("a", "man", macbeth_bigram_dict)
man_appeared = count_phrase_probability("man", "appeared", macbeth_bigram_dict)
print("<a man appeared> : " + str(a_man*man_appeared))

#the old man
the_old = count_phrase_probability("the", "old", macbeth_bigram_dict)
old_man = count_phrase_probability("old", "man", macbeth_bigram_dict)
print("<the old man> : " + str(the_old*old_man))

#second slide of homework
def find_most_pop_second_word(first_word):
    most_common_second_word = None
    print(first_word)
    print(macbeth_bigram_dict[first_word])
    for key, value in macbeth_bigram_dict[first_word].items():
        sorted_values = sorted(macbeth_bigram_dict[first_word].values(), reverse=True)
        if value == sorted_values[0]:
            most_common_second_word = key
            #most_common_second_word = sorted_values[0]
    print(most_common_second_word)


#my way
find_most_pop_second_word("a")
find_most_pop_second_word("the")
find_most_pop_second_word("she")
find_most_pop_second_word("he")
find_most_pop_second_word("they")

#the nltk way
cond_freq_dist = nltk.ConditionalFreqDist(bigrams)
print(cond_freq_dist["a"].max())
print(cond_freq_dist["a"]["man"])
print(cond_freq_dist["the"].max())
print(cond_freq_dist["the"]["time"])
print(cond_freq_dist["she"].max())
print(cond_freq_dist["she"]["ha"])
print(cond_freq_dist["he"].max())
print(cond_freq_dist["he"]["is"])
print(cond_freq_dist["they"].max())
print(cond_freq_dist["they"]["are"])
