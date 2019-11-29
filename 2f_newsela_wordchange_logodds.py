# -*- coding: utf8 -*-

from __future__ import division

import re
import simplejson
import subprocess
import math
import operator
import codecs
from unidecode import unidecode
from collections import Counter
from operator import itemgetter

nversion = 5



jsonfilename = "the_whole_shebang_20140714_sentsfixed.json"
#jsonfilename = "three_newsela_articles.json"

with codecs.open(jsonfilename, mode='r', encoding='utf-8') as jfile:
    jlines = jfile.readlines()

jcontent = " ".join(jlines)
articles = simplejson.loads(jcontent)

count_article = 0

versions_words = [[] for i in range(nversion)]

for article in articles:
    versions = article['articles']
    if len(versions) != 5:
        continue

    count_article += 1

    #if count_article > 5:
    #    continue


    for (v, version) in enumerate(reversed(versions)):
        gradelevel = version['grade_level']
    	sents = version['sentences']
    	title = version['title']

    	words = []
    	for sent in sents:
            if len(sent) > 0:
                sent = re.sub('-', ' ', sent.lower())
                sent = unidecode(sent)
                words = sent.split()
                for word in words:
                    word = word
                    #if not re.search('[a-zA-Z]', word):
                    #if re.search('[a-zA-Z]', word) and not word.isalpha() :
                    #    print word
                    #if not word.isalpha():
                    #    continue
                    versions_words[v].append(word)
                    #if len(word) == 3 :
                    #    allwords_len1.append(word)

total_word_counter = Counter()
versions_word_counter = []
for (version,version_word) in enumerate(versions_words):
    word_counter = Counter(version_word)
    versions_word_counter.append(word_counter)
    total_word_counter += word_counter
    #print len(word_counter)

n_orig = sum(versions_word_counter[0].values())
n_simp = sum(versions_word_counter[4].values())
a0    = sum(total_word_counter.values())

word_logodds = {}
for w in total_word_counter:
    #print word.encode('utf8'), total_word_counter[word]
    aw = total_word_counter[w]
    yw_orig = versions_word_counter[0][w]
    yw_simp = versions_word_counter[4][w]

    p1 = (yw_orig + aw) / (n_orig + a0 - (yw_orig + aw))
    p2 = (yw_simp + aw) / (n_simp + a0 - (yw_simp + aw))

    theta_orig_simp = math.log(p1) - math.log(p2)
    roe_orig_simp_square = (1.0 / (yw_orig + aw)) + (1.0 / (yw_simp + aw))
    log_odds_ratio  = theta_orig_simp / math.sqrt(roe_orig_simp_square)
    word_logodds[w] = log_odds_ratio

sorted_word_logodds = sorted(word_logodds.iteritems(), key=operator.itemgetter(1), reverse=True)
for key, value in sorted_word_logodds:
    print key.encode('utf8'), value, total_word_counter[key], versions_word_counter[0][key], versions_word_counter[4][key]
