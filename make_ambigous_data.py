#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" 
    Create datasets for POS tagger for AAVE with ambiguous learning. 
    This code adds tags to unlabelled data using tag dictionaries. 
    The assignment of tags is dependent on the parameters given. 
    Writes outputs to a .vw-file.

    Many datasets are made with different parameter settings to explore the optimal data configuration for system optimization. 

    Master's thesis project 2015.
    State of the art performance 2015.

"""

from __future__ import division
from collections import defaultdict
from pos_features_partial import taskar12, honnibal13, honnibal13_groups

import argparse
import codecs
import glob
import string 

# NB: count of tags is not implemented in this setup:
#   "if --coarseness == 'tagged_words' use count_of_tags to specify the max number of tags allowed per word in sentence. Can be 

parser = argparse.ArgumentParser(description="""Create dataset for POS tagger for AAVE with ambiguous learning. This code add tags to unlabelled data using tag dictionaries. Outputs to a .vw-file""")
parser.add_argument('--unlabelled', default="data/unlabelled/all-done.txt")
args = parser.parse_args()

punct = set(string.punctuation)

def make_tagdict():
    tagdict = defaultdict(lambda: set())

    # Determine the resources to use based on tagdict conf.
    all_tagdicts = set([td for td in glob.glob("resources/tagdicts/*")])
    for tagdict_conf in set(["all"]): #, "aave", "wiktionary"]):
        
        if tagdict_conf == "aave": 
            tagdict_resources = set([td for td in all_tagdicts if "wik" not in td]) # use dictionaries that are "AAVE-specific", namely Urban dict, Hepsers and list of af-am names.
        elif tagdict_conf == "wiktionary": 
            tagdict_resources = set([td for td in all_tagdicts if "wik" in td]) # use only Wiktionary.
        else: 
            tagdict_resources = all_tagdicts # use all tag tag dictionaries available, AAVE-specific as well as Wiktionary.

        for resource in tagdict_resources:
            data = codecs.open(resource, encoding='UTF-8', errors='replace').readlines()
            
            for line in data:
                elements = line.strip().split('\t')

                if len(elements) == 2:
                    word, tag = elements

                    if len(tag) == 0: continue

                    tagdict[word.lower()].add(tag)

        yield (tagdict, tagdict_conf)

def normalize_word(word):

    if word in punct:
        tag = '.' #:0.0'
    elif word.startswith('@'):
        word= '!@user'
        tag = 'NOUN' #:0.0'
    elif word.startswith('http'):
        word = '!url'
        tag = 'NOUN' #:0.0'
    elif word.startswith('#'):
        word = '!#hashtag'
        tag = 'NOUN' #:0.0'
    elif word.isdigit():
        try:
            word = int(word)
        except ValueError: 
            print('non int word', word)
        if 1800 <= word <= 2100:
            word = "!YEAR"
        else:
            word = "!DIGITS"
        tag = "NUM" #:0.0"
    else: 
        word = word.lower()
        tag = None

    if tag != None:
        tag = set(tag)
    return word, tag

def wordtodict(word, tagdict):
    tags = set()
    word = ''.join(ch for ch in word if ch not in punct)

    if word in set(tagdict.keys()):
        for tag in set(tagdict[word]):
        
            tags.add(tag)

    return tags

def get_tags(word, tagdict):

    tags = None
    word, tags = normalize_word(word)

    if tags == None:
        tags = wordtodict(word, tagdict)
    return tags

def write_to_out(tagdict_conf, coarseness, words, tags, num):
    
    for cost in [0.0, 0.1, 100]:
        out_file = open(f'data/ambiguous/{tagdict_conf}_{coarseness}_{cost}.vw', 'a')
        tags_with_cost = []

        if cost == 100:
            cost == round((100-(100/len(tags)))/100,2)
        
        for n, word in enumerate(words):
            tags_with_cost = [f"{x}:{cost}" for x in tags[n]]

            features = honnibal13(words, [], n)
            out_line = ' '.join(tag for tag in tags_with_cost) + f" 'd-{num}-{n+1}| " + u" ".join(features) + "\n"
            out_file.write(out_line)

        out_file.close()
        

def main():
    """ 
    Annotate unannotated AAVE data with tag dict resources. 
    Fully unsupervised or Weakly supervised.
    """ 

    all_tags = ['ADJ','ADV','ADP','CONJ','DET','NOUN','NUM','PRT','PRON','VERB','X','.']

    # Step 1: make tag dictionary from resources (either all resources, only AAVE specific or only Wiktionary)
    for (tagdict, tagdict_conf) in make_tagdict():
    
        # Step 2: annotate data with tags from tagdict, depending on the annotation configurations

        unlabelled = codecs.open(args.unlabelled, encoding='UTF-8', errors='replace')
        
        for num, line in enumerate(unlabelled):
            words = line.strip().split()
            tags = []
        
            for word in words:
                word_tags = get_tags(word, tagdict)
                tags.append(word_tags)

            assert(len(words) == len(tags))

            # Step 3: Make config dependent representations, add weights, write out. 
            tag_representation = [len(tag) for tag in tags]
            
            config_dependent = {
                "all": [], # assign all tags to words without tags
                "tagged_words_tags": [], # only include words with tags
                "tagged_words_words": [], # only include the corresponding words
            }

            if all([x == 1 for x in tag_representation]):
                write_to_out(tagdict_conf, "unambiguous", words, tags, num)              

            for n, tr in enumerate(tags):
                if len(tr) == 0:
                    config_dependent["all"].append(all_tags)  
                    
                else:
                    config_dependent["all"].append(tags[n])
                    config_dependent["tagged_words_tags"].append(tags[n])
                    config_dependent["tagged_words_words"].append(words[n]) 

            write_to_out(tagdict_conf, "all", words, config_dependent["all"], num)
            write_to_out(tagdict_conf, "tagged_words", config_dependent["tagged_words_words"], config_dependent["tagged_words_tags"], num)

if __name__ == "__main__":
    main()

