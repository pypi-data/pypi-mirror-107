#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ObjectsTokenizer class. Constructed on top of Token and Tokens classes. Token subclasses the Python string, and Tokens catch a collection of Token instances.

Main method is transform or __call__, which receives a string and return list of strings, 
each being a token.
Cut the text in word (string separated by ' '), sentence (string separated by '\n'),
n-grams (succession of words of a given size), char-grams (succession of characters
of a given size) and give back a list of objects having all methods and arguments
of the Python string class, with the extra possibility to add special attributes
to these objects.

"""

import re
from .tokentokens import Token, Tokens


class ObjectsTokenizer():
    """
Tokenizer class making Token objects as element.
This allow in particular to add attribute to the different tokens.
    """
    
    def _check_analyzer(self,analyzer):
        if analyzer not in ['word','sentence','ngram','chargram','document','original']:
            mess = "analyzer must be document, sentence, word, ngram or chargram"
            mess += ', received {}'.format(analyzer)
            raise ValueError(mess)
        self.analyzer = str(analyzer)
        return None
    
    def _check_size(self,size):
        if self.analyzer in ['ngram','chargram'] and not size:
            mess = "size must be provided for ngram and chargram values"
            mess += " of analyzer, received {}".format(size)
            raise ValueError(mess)
        if size:
            self.size = int(size)
        else:
            self.size = None
        return None
    
    def __init__(self,analyzer='word',size=None,generator=False):
        self._check_analyzer(analyzer)
        self._check_size(size)
        self.generator = bool(generator)
        self.tokens = Tokens()
        return None
    
    def __call__(self,doc,shift=0):
        self.tokens = Tokens([Token(start=shift,string=doc),])
        return self._generate()
    
    def _split_doc(self,pattern,flags=0):
        all_tokens = Tokens()
        for token in self.tokens:
            cuts = [(r.start()+token.start,r.end()+token.start)
                    for r in re.finditer(pattern,str(token))]
            tokens = token.split_token(cuts)
            all_tokens += tokens
        self.tokens = all_tokens
        return self.tokens
    
    def _unsplit_doc(self,):
        tokens = self.tokens.copy()
        token = tokens.undo()
        return token
    
    def _generate(self,):
        if self.analyzer=='sentence':
            self._split_doc(r'(\n)+'),
            return self.tokens[::2]
        elif self.analyzer=='word':
            self._split_doc(r'\s+')
            return self.tokens[::2]
        elif self.analyzer=='ngram':
            tokens = self._split_doc(r'\s+')[::2]
            tokens = tokens.join(string=' ')
            tokens_sliced = tokens.slice(size=2*self.size-1,step=2)
            return Tokens(tokens_sliced)
        elif self.analyzer=='chargram':
            tokens = Tokens()
            for token in self.tokens:
                tokens += token.slice(self.size)
            return tokens
        elif self.analyzer in ['document','original']:
            return self.tokens
        else:
            raise AttributeError("Didn't understand the analyzer in transform")
    
    def transform(self,doc,shift=0):
        return self(doc,shift)
    
    def undo(self,):
        if self.analyzer in ['sentence','word','ngram']:
            return self.tokens.undo()
        elif self.analyzer=='chargram':
            return self.tokens.undo(step=self.size)
        elif self.analyzer in ['document','original']:
            return self.tokens[0]
    
    def pipe(self,docs,batch_size=1):
        iterable = iter(docs)
        batch = list(islice(iterable,batch_size))
        while batch:
            tokens = (self.transform(doc) for doc in batch)
            yield tokens
            batch = list(islice(iterable,batch_size))
            


