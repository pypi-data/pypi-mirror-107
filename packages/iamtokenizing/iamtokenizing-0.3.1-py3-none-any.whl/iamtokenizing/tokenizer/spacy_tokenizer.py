#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tokenizer class, adapted for spaCy.

Main method is transform or __call__, which receives a string and return list of strings, 
each being a token.
Cut the text in word (string separated by ' '), sentence (string separeted by '\n'),
n-grams (succession of words of a given size), char-grams (uccession of characters).

"""

from reversible_tokenizer import ReversibleTokenizer as Tokenizer
from spacy.tokens import Doc

class SpacyTokenizer(Tokenizer):
        
    def __init__(self,
                 analyzer='word',
                 size=None,
                 vocab=None):
        super().__init__(analyzer,size)
        self.vocab = vocab
        return None
    
    def transform(self,text):
        words = super().transform(text)
        if self.analyzer in ['word','ngram','sentence']:
            spaces = [True,] * len(words)
        elif self.analyzer in ['chargram','document','original']:
            spaces = [False,] * len(words)
        else:
            raise AttributeError("Didn't understand the analyzer in SpacyTokenizer")
        doc = Doc(self.vocab, words=words, spaces=spaces)
        # doc.text = text # doesn' work
        self.doc = doc 
        return doc
            


