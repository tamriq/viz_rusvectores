#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import gensim
import logging

from genviz import *

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

m = sys.argv[1]
if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)
    
model.init_sims(replace=True)
visualize_dir(sys.argv[2], model, "буква_NOUN", depth=1, topn=5, edge=1)
